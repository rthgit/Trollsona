# Trollsona / Your Troll Alterego

**Tagline:** Summon the little menace living behind your respectable personality.

**Track:** An Adventure in Thousand Token Wood

Trollsona is a Gradio app designed for a Hugging Face Space. It asks for a name, a short confession, a resident menace, a sting level, and whether one useful truth should be included. It returns a theatrical dossier card with:

- a trollsona name
- a playful troll reply
- useful advice
- a deterministic cringe score
- source/fallback notes hidden behind a debug accordion

The default runtime uses a deterministic local fallback, so the demo works without cloud APIs, secrets, or mandatory model downloads.

## Features

- Gradio single-page demo UI
- Hugging Face Space-compatible `app.py`
- Deterministic fallback output path
- Optional local Hugging Face Transformers model path
- Safe roast guard for non-hateful, non-identity-targeted output
- Persona dropdown, sting slider, useful truth checkbox
- Theatrical HTML dossier card plus optional cursed-paperwork debug notes

## Model

Default model id for the optional model path:

```text
Qwen/Qwen2.5-3B-Instruct
```

Model constraint:

```text
small model only, <= 32B parameters
```

By default, model loading is disabled to keep the demo deterministic and reliable:

```bash
TROLLSONA_ENABLE_MODEL=0
```

To opt into the local Transformers path:

```bash
TROLLSONA_ENABLE_MODEL=1
```

If the model import, download, load, or generation fails, the app falls back to the deterministic local generator.

## Stack

- Python
- Gradio
- Hugging Face Spaces
- Hugging Face Transformers, optional runtime path
- PyTorch, optional model backend

No mandatory cloud API is required.

## Run Locally

```bash
pip install -r requirements.txt
python app.py
```

Open:

```text
http://127.0.0.1:7860
```

For the deterministic fallback path:

```bash
TROLLSONA_ENABLE_MODEL=0 python app.py
```

For the optional local model path:

```bash
TROLLSONA_ENABLE_MODEL=1 python app.py
```

## Hugging Face Space Deploy

Required files:

- `app.py`
- `requirements.txt`
- `README.md`
- `assets/style.css`

Space SDK:

```text
Gradio
```

Secrets required:

```text
[ASSENTE]
```

Space link:

```text
[DA COMPLETARE]
```

GitHub repo:

```text
[DA COMPLETARE]
```

## Safety

Trollsona is a roast generator, but the roast target is limited to harmless style, habits, project energy, and behavior. It avoids:

- hate or protected-class targeting
- identity-based insults
- threats
- self-harm content
- sexual content
- heavy personal attacks

If generated model output fails the safety guard, the app replaces it with a safe fallback card.

## Hackathon Fit

- Built as a Gradio app for Hugging Face Space
- Fits the track: An Adventure in Thousand Token Wood
- Uses a small optional local model path under the <=32B limit
- Demo-friendly output: whimsical, short, structured, and shareable
- No mandatory cloud API or secret
- Deterministic fallback keeps the demo stable for judging

## Known Limits

- Public Space link: [DA COMPLETARE]
- Public GitHub repo link: [DA COMPLETARE]
- Demo video: [DA COMPLETARE]
- Codex-attributed commits: [ASSENTE], because the current folder is not a Git repository
- Exact model behavior across hardware: [AMBIGUO], because hardware/runtime are not specified
