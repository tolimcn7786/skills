# Troubleshooting

| Symptom | Cause | Fix |
|---|---|---|
| `RuntimeError: assets not ready` on download | Program is still generating after compile | The SDK polls automatically for up to 30s. If it still fails, retry shortly or recompile. |
| `httpx.HTTPStatusError: 422` on compile | Spec too short (<10 chars) or request validation failed | Lengthen the spec / fix the request shape. |
| `httpx.HTTPStatusError: 429` | Hosted compile rate limit exceeded | Wait, or sign in (`PAW_API_KEY`) for higher limits. |
| GPU / Metal errors on load | GPU backend unavailable or incompatible | Set `PAW_GPU_LAYERS=0` or pass `n_gpu_layers=0` to force CPU. |
| Output is free-form, not the label you wanted | Spec lacks an explicit output constraint | Add "Return ONLY one of: X, Y, Z" and a few `Input/Output` examples. |
| First call is slow | Loading the shared base model | Expected (~1-5s once). Subsequent calls are ~0.05-0.5s; offline after first download. |
| Input errors / truncation | Spec + input + output exceed the ~2048-token window | Trim the spec or pre-chunk long inputs. |

Anonymous compile limits: 20/hr, 1 concurrent. Authenticated: 60/hr, 2 concurrent.
Inference is local and not rate-limited.

Canonical, current docs: https://programasweights.com/AGENTS.md and
https://programasweights.readthedocs.io
