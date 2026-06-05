# Trollsona Submission Pack

## Submission Checklist

| requirement | status | proof | missing action |
|---|---|---|---|
| Public GitHub repo | DONE | https://github.com/rthgit/Trollsona | None |
| Codex-attributed commits | DONE | `0428072`; final docs commit in latest Git history after this pass | None |
| Space README links to repo | DONE | `README.md` contains repo URL | None |
| Hugging Face Space deploy | [DA COMPLETARE] | No Space URL present | Create Space and push/upload files |
| Space link | [DA COMPLETARE] | README placeholder | Replace after deploy |
| Demo video | [DA COMPLETARE] | No video link/file present | Record 45-60s demo |
| Social post | [DA COMPLETARE] | Draft below | Publish and add final link if required |
| Gradio app | DONE | `app.py` defines `gr.Blocks` app | None |
| Small model <=32B | DONE | Optional model id: `Qwen/Qwen2.5-3B-Instruct` | None |
| Deterministic fallback | DONE | Local QA: repeated generation matched | None |
| Debug hidden by default | DONE | Source/fallback live in `See the cursed paperwork` | None |
| No mandatory cloud API | DONE | Default fallback requires no secrets | None |

## Demo Video Script

Target length: 45-60 seconds.

| timestamp | action | what it shows | suggested line |
|---|---|---|---|
| 0:00-0:05 | Open the Space | Trollsona hero, badges, dark ritual UI | "This is Trollsona, a tiny ritual for summoning your troll alter ego." |
| 0:05-0:15 | Enter name and lore | `What do they call you?`, `Confess your little lore` | "Give it a name and a little confession." |
| 0:15-0:23 | Pick menace and sting | Dropdown, slider, useful truth checkbox | "Choose the resident menace and how hard the roast should sting." |
| 0:23-0:32 | Click `Summon Trollsona` | End-to-end generation | "The app returns a theatrical dossier, not a raw chatbot answer." |
| 0:32-0:45 | Show result card | Name, roast, useful slap, goblin meter | "You get a trollsona name, one sharp line, one useful slap, and a deterministic goblin meter." |
| 0:45-0:53 | Optional: open paperwork | Debug source/fallback hidden by default | "Debug info stays in the cursed paperwork, out of the main experience." |
| 0:53-0:60 | Close on constraints | Gradio, small model, deterministic fallback | "It is built for Gradio Spaces, small-model constraints, and reliable demos." |

## Social Post Draft

Hook: I built a little ritual that summons the troll living behind your respectable personality.

Description: Trollsona turns a short confession into a theatrical alter-ego dossier: trollsona name, playful roast, one useful slap, and a deterministic goblin meter.

Tech note: Built for Build Small Hackathon as a Gradio Hugging Face Space. Default path is deterministic fallback; optional local Transformers model path stays under the `<=32B` small-model constraint.

Links:

- Space: [DA COMPLETARE]
- GitHub: https://github.com/rthgit/Trollsona

CTA: Try it, summon your menace, and share the dossier.

## Release QA

| test | command/action | expected result | status |
|---|---|---|---|
| Python compile | `python -B -m py_compile app.py` | no syntax errors | DONE |
| Deterministic fallback | run `generate_trollsona(...)` twice | identical structured output | DONE |
| Local Gradio launch | `python app.py` | app opens on `127.0.0.1:7860` | DONE in local QA |
| Input-full generation | fill name + lore + summon | result card renders | DONE in local QA |
| Input-minimal generation | empty name/lore | output still complete | DONE |
| Debug default | load page | source/fallback hidden | DONE |
| Visual contrast | inspect input/dropdown/checkbox/CTA/card | readable UI | DONE |
| Git status | `git status --short --ignored` | only ignored `.env` / QA screenshot remain | DONE |
| README repo link | inspect README | GitHub URL present | DONE |
| Space build | Hugging Face build logs | Space starts successfully | [DA COMPLETARE] |
| Browser test on Space | open public Space and summon | card renders on hosted Space | [DA COMPLETARE] |

## Final Ship Plan

| step | owner | output | done criteria | priority |
|---|---|---|---|---|
| 1 | Codex | Final README and submission docs | Docs committed | P0 |
| 2 | Codex/User | GitHub push | `rthgit/Trollsona` contains latest commits | P0 |
| 3 | User | Hugging Face Space | Public Space URL opens app | P0 |
| 4 | User | README Space link | `[DA COMPLETARE]` replaced with Space URL | P0 |
| 5 | User | Demo video | 45-60s video available | P1 |
| 6 | User | Social post | Published post with links | P1 |
| 7 | User | Submission form | All required URLs submitted | P0 |
