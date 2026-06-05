# Trollsona Submission Pack

## Submission Checklist

| requirement | status | proof | missing action |
|---|---|---|---|
| Public GitHub repo | DONE | https://github.com/rthgit/Trollsona | None |
| Codex-attributed commits | DONE | `3fe2db1`, `4f196a6`, `8a1b09d` | None |
| Space README links to repo | DONE | `README.md` contains repo URL | None |
| Hugging Face Space deploy | DONE | https://huggingface.co/spaces/RthItalia/Trollsona | None |
| Space link | DONE | `README.md` contains https://huggingface.co/spaces/RthItalia/Trollsona | None |
| Space model variables | DONE | `.env.example` documents `TROLLSONA_ENABLE_MODEL=1`, `TROLLSONA_MODEL_ID=RthItalia/nano_compact_3b_qkvfp16`, `TROLLSONA_FALLBACK_MODEL_ID=Qwen/Qwen2.5-0.5B-Instruct` | Configure the same variables in Space settings if overriding defaults |
| Demo video | [DA COMPLETARE] | No video link/file present | Record 45-60s demo |
| Social post | [DA COMPLETARE] | Draft below contains Space/GitHub URLs | Publish and add final link if required |
| Gradio app | DONE | `app.py` defines `gr.Blocks` app | None |
| Small model <=32B | DONE | Primary model id: `RthItalia/nano_compact_3b_qkvfp16`; fallback model id: `Qwen/Qwen2.5-0.5B-Instruct` | None |
| Transformers model path | DONE | `TROLLSONA_ENABLE_MODEL=1` in Space variables; `AutoModelForCausalLM.from_pretrained(..., trust_remote_code=True)` implemented | None |
| Deterministic fallback | DONE | Fallback remains available with `TROLLSONA_ENABLE_MODEL=0`, unavailable CUDA, model failure, or invalid model output | None |
| Debug hidden by default | DONE | Source/fallback live in `See the cursed paperwork` | None |
| No mandatory cloud API | DONE | Public HF model path and fallback require no app secrets | None |

## Demo Video Script

Target length: 45-60 seconds.

Recommended tested input:

```text
Name: Alex
Lore: I start productivity systems and then reorganize the labels forever.
Persona: Dungeon Intern
Spice: 4
Advice: on
```

Hosted test result: `Source: transformers_model`; runtime `Qwen/Qwen2.5-0.5B-Instruct` as CPU fallback model.

| timestamp | action | what it shows | suggested line |
|---|---|---|---|
| 0:00-0:05 | Open the Space | Trollsona hero, badges, dark ritual UI | "This is Trollsona: a small-model goblin that turns your personal lore into a cursed alter ego." |
| 0:05-0:15 | Enter name and lore | `What do they call you?`, `Confess your little lore` | "I give it a name and a very specific little confession." |
| 0:15-0:23 | Pick menace and sting | `Dungeon Intern`, spice `4`, advice on | "Then I choose the resident menace and how hard it should sting." |
| 0:23-0:32 | Click `Summon Trollsona` | End-to-end generation | "It summons a theatrical dossier instead of a plain chatbot answer." |
| 0:32-0:42 | Show result card | Trollsona name, roast, useful slap, goblin meter | "You get a name, a roast, one useful slap, and the goblin meter." |
| 0:42-0:50 | Open paperwork | `Source: transformers_model` and CPU runtime | "The model details stay hidden in the cursed paperwork until you ask for them." |
| 0:50-0:58 | Show README/Codex Track | Space, GitHub, model cascade, Codex commits | "Built as a Gradio Space with a small-model cascade and Codex-tracked commits." |
| 0:58-1:00 | Close on Space | Final result card or Space URL | "Tiny model, giant attitude." |

## Social Post Draft

Hook: I built a little ritual that summons the troll living behind your respectable personality.

Description: Trollsona turns a short confession into a theatrical alter-ego dossier: trollsona name, playful roast, one useful slap, and a goblin meter.

Tech note: Built for Build Small Hackathon as a Gradio Hugging Face Space. The primary model is `RthItalia/nano_compact_3b_qkvfp16`, derived from `Qwen/Qwen2.5-3B-Instruct` and under the `<=32B` small-model constraint. A Qwen 0.5B model and deterministic fallback remain as reliability guards.

Links:

- Space: https://huggingface.co/spaces/RthItalia/Trollsona
- GitHub: https://github.com/rthgit/Trollsona

CTA: Try it, summon your menace, and share the dossier.

## Release QA

| test | command/action | expected result | status |
|---|---|---|---|
| Python compile | `python -B -m py_compile app.py` | no syntax errors | DONE |
| Model path implemented | inspect `app.py` | Space sets `TROLLSONA_ENABLE_MODEL=1`; `from_pretrained(..., trust_remote_code=True)` path present | DONE |
| Deterministic fallback | run `generate_trollsona(...)` twice | identical structured output | DONE |
| Local Gradio launch | `python app.py` | app opens on `127.0.0.1:7860` | DONE in local QA |
| Input-full generation | fill name + lore + summon | result card renders | DONE in local QA |
| Input-minimal generation | empty name/lore | output still complete | DONE |
| Debug default | load page | source/fallback hidden | DONE |
| Visual contrast | inspect input/dropdown/checkbox/CTA/card | readable UI | DONE |
| Git status | `git status --short --ignored` | only ignored `.env` / QA screenshot remain | DONE |
| README repo link | inspect README | GitHub URL present | DONE |
| Space build | Hugging Face runtime API | `stage=RUNNING`, `requested=cpu-basic` | DONE |
| Browser test on Space | Playwright on public Space | card renders; debug source/fallback hidden until accordion opens | DONE |
| Hosted model-backed generation | Playwright on public Space, then open `See the cursed paperwork` | `Source: transformers_model`; runtime `Qwen/Qwen2.5-0.5B-Instruct` as `fallback_model` on CPU; fallback note reports primary `RthItalia/nano_compact_3b_qkvfp16` skipped because CUDA is unavailable | DONE |

## Final Ship Plan

| step | owner | output | done criteria | priority |
|---|---|---|---|---|
| 1 | Codex | Final README and submission docs | Docs committed | P0 |
| 2 | Codex/User | GitHub push | `rthgit/Trollsona` contains latest commits | P0 |
| 3 | Codex | Hugging Face Space | Public Space URL opens app | P0 |
| 4 | Codex | README Space link | Space URL is present in `README.md` | P0 |
| 5 | User | Demo video | 45-60s video available | P1 |
| 6 | User | Social post | Published post with links | P1 |
| 7 | User | Submission form | All required URLs submitted | P0 |
