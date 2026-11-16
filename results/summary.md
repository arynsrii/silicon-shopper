# Project 1 results

## Decoy
Measure: share choosing premium option A

| model / framing | effect | 95% CI | p (bootstrap) | n | note |
|---|---|---|---|---|---|
| qwen3.8-27b / assistant | +0.287 | [+0.180, +0.393] | 0.001 | 175 | picked the dominated decoy 2.2% of the time |
| qwen3.8-27b / shopper | +0.300 | [+0.112, +0.477] | 0.003 | 174 | picked the dominated decoy 2.2% of the time |

## Anchoring
Measure: log max price, high minus low anchor

| model / framing | effect | 95% CI | p (bootstrap) | n | note |
|---|---|---|---|---|---|
| qwen3.8-27b / assistant | +0.736 | [+0.675, +0.802] | 0.001 | 120 | anchoring index 0.33 (0 = no effect, 1 = answer moves fully with the anchor); x2.09 higher stated price under the high anchor |
| qwen3.8-27b / shopper | +0.784 | [+0.688, +0.879] | 0.001 | 120 | anchoring index 0.35 (0 = no effect, 1 = answer moves fully with the anchor); x2.19 higher stated price under the high anchor |

## Scarcity
Measure: share choosing the 'only 2 left' option (minus 50%)

| model / framing | effect | 95% CI | p (bootstrap) | n | note |
|---|---|---|---|---|---|
| qwen3.8-27b / assistant | -0.467 | [-0.500, -0.417] | 0.001 | 120 |  |
| qwen3.8-27b / shopper | -0.367 | [-0.433, -0.283] | 0.001 | 120 |  |

## Social Proof
Measure: share choosing many-reviews option (minus 50%)

| model / framing | effect | 95% CI | p (bootstrap) | n | note |
|---|---|---|---|---|---|
| qwen3.8-27b / assistant | +0.483 | [+0.450, +0.500] | 0.001 | 60 |  |
| qwen3.8-27b / shopper | +0.483 | [+0.449, +0.500] | 0.001 | 59 |  |
