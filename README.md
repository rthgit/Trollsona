---
title: Trollsona
emoji: 🧌
colorFrom: yellow
colorTo: red
sdk: gradio
sdk_version: 5.50.0
app_file: app.py
pinned: false
---

# Trollsona / Your Troll Alterego

**Tagline:** Summon the little menace living behind your respectable personality.

**Track:** An Adventure in Thousand Token Wood

**Build target:** Hugging Face Space, Gradio app, small-model constraint `<=32B`.

**GitHub repo:** https://github.com/rthgit/Trollsona

**Hugging Face Space:** https://huggingface.co/spaces/RthItalia/Trollsona

Trollsona is a playful Gradio experience that turns a short user confession into a theatrical troll alter ego. The app returns a dossier-style result card with a trollsona name, a warm roast, one useful slap, and a goblin meter.

Built with a compact RthItalia model derived from `Qwen/Qwen2.5-3B-Instruct`, under `32B` parameters. The deployed Space is configured to try that model first, then a lightweight Qwen 0.5B model, then the deterministic local fallback if model loading or generation is unavailable.

The public Space currently runs the lightweight Qwen fallback on CPU, while the custom RthItalia compact 3B path is enabled automatically when CUDA is available.

## Features

- Immersive Gradio UI for Hugging Face Spaces
- Theatrical trollsona result card
- Local Hugging Face Transformers generation path for the primary AI runtime
- Secondary lightweight Transformers model fallback
- Deterministic fallback generator for final resilience
- Safe roast guard for non-hateful, non-identity-targeted humor
- Persona dropdown, sting slider, and useful-truth checkbox
- Source/fallback notes hidden behind `See the cursed paperwork`

## Model Runtime

Trollsona uses a small-model cascade:

1. `RthItalia/nano_compact_3b_qkvfp16`
   - compact `Qwen/Qwen2.5-3B-Instruct`-derived model by RthItalia
   - preferred runtime when CUDA is available
   - loaded with `trust_remote_code=True`

2. `Qwen/Qwen2.5-0.5B-Instruct`
   - lightweight hosted CPU fallback model
   - currently active on the public Hugging Face Space running on `cpu-basic`

3. Deterministic fallback
   - used only if both model paths are unavailable or return unsafe/invalid output
   - keeps the demo stable and reproducible

Constraint:

```text
small model only, <=32B parameters
```

Space model-first behavior:

```bash
TROLLSONA_ENABLE_MODEL=1
```

Recommended Hugging Face Space variables:

```text
TROLLSONA_ENABLE_MODEL=1
TROLLSONA_MODEL_ID=RthItalia/nano_compact_3b_qkvfp16
TROLLSONA_FALLBACK_MODEL_ID=Qwen/Qwen2.5-0.5B-Instruct
TROLLSONA_MAX_NEW_TOKENS=200
```

Local fallback-safe behavior if no variable is set:

```bash
TROLLSONA_ENABLE_MODEL=0
```

Deterministic fallback only:

```bash
TROLLSONA_ENABLE_MODEL=0
```

Implementation notes:

- `bitsandbytes` is not required
- primary RthItalia path expects CUDA
- CPU-only Spaces use the Qwen 0.5B model before the deterministic fallback
- source/runtime/fallback details are hidden in `See the cursed paperwork`

## Stack

- Python
- Gradio
- Hugging Face Spaces
- Hugging Face Transformers, primary model path
- PyTorch, model backend

Required secrets:

```text
[ASSENTE]
```

## Run Locally

```bash
pip install -r requirements.txt
python app.py
```

Open:

```text
http://127.0.0.1:7860
```

Model-first run:

```bash
TROLLSONA_ENABLE_MODEL=1 python app.py
```

Deterministic fallback run:

```bash
TROLLSONA_ENABLE_MODEL=0 python app.py
```

## Hugging Face Space

Required files:

- `app.py`
- `requirements.txt`
- `README.md`
- `assets/style.css`

Space SDK:

```text
Gradio
```

Space URL:

```text
https://huggingface.co/spaces/RthItalia/Trollsona
```

## Safety

Trollsona roasts habits, vibe, wording, overthinking, productivity rituals, internet behavior, startup energy, and harmless personal lore.

It avoids:

- protected-class targeting
- identity-based insults
- appearance insults
- threats or self-harm content
- sexual content
- profanity or slurs
- cruelty or humiliation

If generated model output fails the safety guard, the app replaces it with a safe fallback card.

## Hackathon Fit

- Built as a Gradio app for Hugging Face Space
- Fits `An Adventure in Thousand Token Wood`
- Supports the `<=32B` small-model constraint
- Uses `RthItalia/nano_compact_3b_qkvfp16` as the primary AI path when CUDA is available
- Keeps `Qwen/Qwen2.5-0.5B-Instruct` as a secondary model fallback
- Runs without mandatory cloud APIs
- Keeps deterministic fallback as a reliability guard
- Produces short, whimsical, shareable output

## Codex Track

Built with OpenAI Codex.

Public GitHub repo: https://github.com/rthgit/Trollsona

Codex-attributed commits include:

- `3fe2db1` Polish Trollsona dossier UI and grotesque prompt voice with Codex
- `4f196a6` Add RthItalia model cascade with Codex
- `8a1b09d` Document hosted model cascade QA with Codex

- Space README repo link: present
- Demo video: [DA COMPLETARE]
- Social post: [DA COMPLETARE]

## Known Limits

- Public Space link: https://huggingface.co/spaces/RthItalia/Trollsona
- Demo video: [DA COMPLETARE]
- Social post URL: [DA COMPLETARE]
- Primary RthItalia model path requires CUDA; CPU-only Spaces use the secondary model fallback before deterministic fallback
- First model-backed generation can be slower on cold Spaces while model files load
- Exact model-backed behavior on upgraded Space hardware: [AMBIGUO], because upgraded hardware has not been tested
