# Silicon Shopper 2.0 — Flagship Project Plan

**Stage:** Planning / research design. The existing 2026 experiment remains the evidence base. New v2 studies, products and human benchmarks are PROPOSED, not completed.

**Research theme:** Behavioral economics of AI-mediated commerce.

**One-sentence thesis:** As purchasing moves from humans to AI assistants, seemingly familiar marketing signals can be interpreted differently depending on the goal delegated to the agent.

## What we are building

One evidence-led project with three mutually reinforcing artifacts:

1. **Research:** A controlled multi-model study about scarcity, fulfillment information and buyer objectives, followed by deconfounded replications of other choice-architecture effects.
2. **Tool:** A lightweight, reproducible AI shopping-choice experiment runner and public results explorer. Start with static offline results; only add live multi-model comparisons after model costs, prompts, error handling and controls are validated.
3. **Communication:** An accessible executive brief, a transparent technical report, and an illustrated project case study.

A *research study*, a *research engineering tool*, and a *business-relevant explanation* are complementary accomplishments. Do not describe a proposed tool as shipped or a working paper as published.

## Audiences and credible evidence

| Audience | Show | Avoid |
|---|---|---|
| Business-school faculty | Literature gap, hypotheses, experimental design, statistics, replication, limitations | 'I proved AI is irrational' |
| Startup founders | Customer insight, tangible demo, end-to-end execution, practical implication | Startup traction or adoption without users |
| Corporate / product internships | Python automation, analytics, randomized testing, dashboard, documentation | Generic 'AI expert' positioning |
| Fellowships, cohorts and conferences | Personal curiosity, independent initiative, consumer trust and market implications, outreach to stakeholders | Empty thought leadership or invented social impact |

## Sequence and acceptance criteria

### Phase 0 — Integrity audit (first)
- Reproduce every v1 table and plot from the exact committed data using a clean environment.
- Report counts of attempted, successful, parseable, valid and included observations by condition.
- Correct the clustered-bootstrap implementation for anchoring and ensure sensitivity tests use the appropriate unit of randomization.
- State whether every reported number uses trials, choices or API calls as denominator.
- Publish an errata or revised v1 summary if the audit changes any claim.
- Add automated tests and a CI workflow.

### Phase 1 — Focused discovery (proposed)
- Lock a clearly documented causal design for scarcity + delivery risk + delegated buyer objective.
- Conduct a small *format* pilot before confirmatory collection. Fix the prompt/stimuli and hypothesis plan before collecting the main sample.
- Run across at least two model families if budget permits, recording provider, exact model ID, settings, date, costs, raw outputs and parsing failures.
- Use proper product-clustered inference and product-level held-out robustness.
- If not enough independent categories, be explicit about the generalization limit.

### Phase 2 — Build usable artifact
- Refactor experiments into configuration-driven modules with schema validation and tests.
- Offer a results viewer with documented data provenance, condition filters, model comparisons and uncertainty intervals.
- Optionally add a non-transactional storefront mockup: users can select between simulated product listings, but it does not place orders.

### Phase 3 — Human evidence (optional, not a requirement to report valid AI-only findings)
- Launch a consented human-choice task only after defining sample, hypothesis, study procedures, privacy and power/precision rationale.
- Distinguish hypothetical stated choices from real purchases and convenience samples from representative populations.

### Phase 4 — Public outputs
- GitHub: clear landing page, reproducible environment, sample data, methods, results, tests, demo screenshots.
- Research: 6–10 page working paper and technical appendix; publication is aspirational, not assumed.
- Employers: 1-page experiment/analytics case study and functional demo.
- Programs: a first-person narrative of the question, surprise, follow-up, learning and real-world importance.
- Outreach: professor-specific 1-paragraph research overlap and concrete offer of research assistance.

## Metrics that matter

Track actual measurable outputs: number of verified model families, number of *independent* products/categories, calls and valid responses, model/condition coverage, reproducibility checks, number of finished tests, demo functionality, outside technical reviews, and sample size/response rate for any human study. Never put aspirational metrics on a CV.

## Prior research to engage, not claim to supersede
- MIT ABxLab: https://abxlab.media.mit.edu/
- Columbia ACES: https://business.columbia.edu/faculty/research/what-your-ai-agent-buying-evaluation-implications-and-emerging-questions-agentic-e
- Wharton agentic shopping study: https://gail.wharton.upenn.edu/research-and-insights/technical-report-agentic-shopping/
- Chicago Booth Center for Applied AI (behavioral science): https://www.chicagobooth.edu/research/center-for-applied-artificial-intelligence/research/our-faculty-research/behavioral-science
