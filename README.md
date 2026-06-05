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

Trollsona is a playful Gradio experience that turns a short user confession into a theatrical troll alter ego. The app returns a dossier-style result card with a trollsona name, a warm roast, one useful slap, and a deterministic goblin meter.

The default runtime uses a deterministic local fallback, so the demo works without mandatory cloud APIs, secrets, or model downloads. An optional Hugging Face Transformers path is available behind an environment flag.

## Features

- Immersive Gradio UI for Hugging Face Spaces
- Theatrical trollsona result card
- Deterministic fallback generator
- Optional local Hugging Face Transformers generation path
- Safe roast guard for non-hateful, non-identity-targeted humor
- Persona dropdown, sting slider, and useful-truth checkbox
- Source/fallback notes hidden behind `See the cursed paperwork`

## Model And Runtime

Default optional model:

```text
Qwen/Qwen2.5-3B-Instruct
```

Constraint:

```text
small model only, <=32B parameters
```

Default behavior:

```bash
TROLLSONA_ENABLE_MODEL=0
```

Optional local Transformers path:

```bash
TROLLSONA_ENABLE_MODEL=1
```

If the model import, download, load, or generation fails, the app falls back to the deterministic local generator.

## Stack

- Python
- Gradio
- Hugging Face Spaces
- Hugging Face Transformers, optional
- PyTorch, optional model backend

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

Deterministic fallback:

```bash
TROLLSONA_ENABLE_MODEL=0 python app.py
```

Optional local model path:

```bash
TROLLSONA_ENABLE_MODEL=1 python app.py
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
- Runs without mandatory cloud APIs
- Keeps the default demo deterministic
- Produces short, whimsical, shareable output

## Codex Track

- Public GitHub repo: https://github.com/rthgit/Trollsona
- Codex-attributed polish commit: `0428072`
- Deploy documentation commit: `Add deployed Space link for Trollsona submission`
- Space README repo link: present
- Demo video: [DA COMPLETARE]
- Social post: [DA COMPLETARE]

## Known Limits

- Public Space link: https://huggingface.co/spaces/RthItalia/Trollsona
- Demo video: [DA COMPLETARE]
- Social post URL: [DA COMPLETARE]
- Exact optional-model behavior on upgraded Space hardware: [AMBIGUO], because the optional Transformers path is disabled by default and has not been tested on upgraded hardware
