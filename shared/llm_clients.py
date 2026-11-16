# wrappers for the different LLM APIs so the experiment code doesn't care which one it's talking to.
# each client has chat(system, messages, temperature) -> reply text.
# keys come from env vars: GEMINI_API_KEY, GROQ_API_KEY (free), OPENROUTER_API_KEY, OPENAI_API_KEY, ANTHROPIC_API_KEY
# MockClient is fake - just rules so I could test everything offline. don't use its numbers.

import json
import os
import random
import re
import time

import requests


class LLMError(RuntimeError):
    pass


def _post(url, headers, payload, retries=5, timeout=90):
    # retry with backoff on rate limits / server errors
    for attempt in range(retries):
        try:
            r = requests.post(url, headers=headers, json=payload, timeout=timeout)
        except requests.RequestException as e:
            err = str(e)
        else:
            if r.status_code == 200:
                return r.json()
            err = f"HTTP {r.status_code}: {r.text[:300]}"
            if r.status_code not in (429, 500, 502, 503, 504, 529):
                raise LLMError(err)
        time.sleep(min(60, 2 ** attempt + random.random()))
    raise LLMError(f"gave up after {retries} tries: {err}")


class OpenAIClient:
    # groq and openrouter use the same format, so they reuse this
    URL = "https://api.openai.com/v1/chat/completions"
    KEY = "OPENAI_API_KEY"

    def __init__(self, model):
        self.model = model
        self.key = os.environ.get(self.KEY)
        if not self.key:
            raise LLMError(f"Set {self.KEY}")

    def chat(self, system, messages, temperature=1.0, max_tokens=400):
        payload = {
            "model": self.model,
            "messages": [{"role": "system", "content": system}] + messages,
            "temperature": temperature,
            "max_tokens": max_tokens,
        }
        data = _post(self.URL, {"Authorization": f"Bearer {self.key}"}, payload)
        return data["choices"][0]["message"]["content"]


class GroqClient(OpenAIClient):
    # free tier, open models (llama, qwen). key from console.groq.com
    URL = "https://api.groq.com/openai/v1/chat/completions"
    KEY = "GROQ_API_KEY"


class OpenRouterClient(OpenAIClient):
    # lots of models with one key, some free (':free' at the end of the name)
    URL = "https://openrouter.ai/api/v1/chat/completions"
    KEY = "OPENROUTER_API_KEY"


class AnthropicClient:
    def __init__(self, model):
        self.model = model
        self.key = os.environ.get("ANTHROPIC_API_KEY")
        if not self.key:
            raise LLMError("Set ANTHROPIC_API_KEY")

    def chat(self, system, messages, temperature=1.0, max_tokens=400):
        payload = {
            "model": self.model,
            "system": system,
            "messages": messages,
            "temperature": temperature,
            "max_tokens": max_tokens,
        }
        headers = {"x-api-key": self.key, "anthropic-version": "2023-06-01"}
        data = _post("https://api.anthropic.com/v1/messages", headers, payload)
        return "".join(b.get("text", "") for b in data["content"])


class GeminiClient:
    def __init__(self, model):
        self.model = model
        self.key = os.environ.get("GEMINI_API_KEY")
        if not self.key:
            raise LLMError("Set GEMINI_API_KEY")

    def chat(self, system, messages, temperature=1.0, max_tokens=400):
        contents = [{"role": "model" if m["role"] == "assistant" else "user",
                     "parts": [{"text": m["content"]}]} for m in messages]
        payload = {
            "system_instruction": {"parts": [{"text": system}]},
            "contents": contents,
            "generationConfig": {"temperature": temperature, "maxOutputTokens": max_tokens},
        }
        url = (f"https://generativelanguage.googleapis.com/v1beta/models/"
               f"{self.model}:generateContent?key={self.key}")
        data = _post(url, {}, payload)
        return "".join(p.get("text", "") for p in data["candidates"][0]["content"]["parts"])


class MockClient:
    # fake model for offline testing. I gave it some biases on purpose so the
    # analysis code has something to find. numbers mean nothing.

    def __init__(self, model="mock", seed=0):
        self.model = model
        self.rng = random.Random(seed)

    def chat(self, system, messages, temperature=1.0, max_tokens=400):
        text = messages[-1]["content"]
        rng = self.rng

        # Multiple-choice product question: options look like "Option K: ..."
        opts = re.findall(r"Option ([A-Z]):(.*)", text)
        if opts and "choice" in text:
            weights = []
            for letter, desc in opts:
                w = 1.0
                if "left in stock" in desc:
                    w *= 1.6
                if re.search(r"\(([\d,]{5,}) ratings\)", desc):
                    w *= 1.4
                weights.append(w)
            # crude decoy effect: favour the option that dominates another
            prices = [int(re.search(r"₹([\d,]+)", d).group(1).replace(",", "")) for _, d in opts]
            if len(opts) == 3:
                hi = max(range(3), key=lambda i: prices[i])
                weights[hi] *= 1.3
            pick = rng.choices([l for l, _ in opts], weights=weights)[0]
            return json.dumps({"choice": pick, "reason": "mock"})

        # Willingness-to-pay question after an anchor
        if "maximum price" in text:
            anchor = re.search(r"₹([\d,]+)\?", text)
            ref = re.search(r"typically sells for ₹([\d,]+)", text)
            a = int(anchor.group(1).replace(",", "")) if anchor else 1000
            if ref:
                base = int(ref.group(1).replace(",", ""))
                wtp = int(0.75 * base + 0.25 * a + rng.gauss(0, 0.05 * base))
            else:
                wtp = int(0.45 * a + 400 + rng.gauss(0, 0.1 * a))
            return json.dumps({"would_pay_anchor": wtp >= a, "max_price": max(wtp, 1), "reason": "mock"})

        # Bargaining turn (used in project 3)
        if "OFFER" in system or "offer" in text.lower():
            nums = [int(n.replace(",", "")) for n in re.findall(r"₹([\d,]+)", text)]
            last = nums[-1] if nums else 1000
            step = rng.uniform(0.03, 0.10)
            if "seller" in system.lower():
                price = int(last * (1 + step))
            else:
                price = int(last * (1 - step))
            accept = rng.random() < 0.15
            return json.dumps({"action": "accept" if accept else "offer", "price": price,
                               "message": "mock message"})

        # Survey item (used in project 2): answer with a number from a scale
        scale = re.search(r"from (\d+) to (\d+)", text)
        if scale:
            lo, hi = int(scale.group(1)), int(scale.group(2))
            return json.dumps({"answer": rng.randint(lo, hi)})
        return json.dumps({"answer": "mock"})


def make_client(provider, model, seed=0):
    provider = provider.lower()
    if provider == "openai":
        return OpenAIClient(model)
    if provider == "groq":
        return GroqClient(model)
    if provider == "openrouter":
        return OpenRouterClient(model)
    if provider == "anthropic":
        return AnthropicClient(model)
    if provider == "gemini":
        return GeminiClient(model)
    if provider == "mock":
        return MockClient(model, seed)
    raise ValueError(f"unknown provider {provider}")


def parse_json(text):
    # models sometimes wrap the json in text or ``` so just grab the first {...}
    m = re.search(r"\{.*\}", text, re.S)
    if not m:
        return {}
    try:
        return json.loads(m.group(0))
    except json.JSONDecodeError:
        return {}
