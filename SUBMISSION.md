# Trollsona Submission Pack

## Demo Script

| scene | action | what it shows | estimated duration |
|---|---|---|---|
| Opening | Open the Hugging Face Space | Project name, track, Gradio UI | 5s |
| User input | Enter name and short personal lore | Simple input flow | 10s |
| Controls | Pick resident menace, set sting level, keep useful truth enabled | Persona dropdown, slider, checkbox | 8s |
| Generate | Click `Generate Trollsona` | End-to-end Gradio callback | 5s |
| Trollsona output | Show generated card | Trollsona name, roast, output styling | 10s |
| Useful advice | Point to advice tile | Joke plus actionable suggestion | 5s |
| Cursed paperwork | Open debug accordion only if needed | Deterministic data contract hidden from primary UI | 5s |
| Close | Mention fallback and no mandatory cloud API | Reliability for judging | 7s |

Estimated total: 55s.

## Social Post Draft

Hook: Meet your troll alter ego.

What it does: Trollsona turns a tiny user profile into a theatrical roast dossier with a trollsona name, one useful slap, and a deterministic cringe meter.

Small model constraint: Built for the small-model track with an optional local Transformers model path under <=32B parameters, plus a deterministic fallback for reliable demos.

Space link: [DA COMPLETARE]

GitHub repo: [DA COMPLETARE]

Call to action: Try it, share your Trollsona, and see how much bridge-certified cringe your side quests produce.

## Codex Track Checklist

| requirement | status | proof | missing action |
|---|---|---|---|
| Hugging Face Space deploy | [DA COMPLETARE] | Local Gradio launch passed in QA | Create Space and upload files |
| Public GitHub repo | [ASSENTE] | `.git` is absent in current folder | Initialize/publish repo |
| Codex-attributed commits | [ASSENTE] | `.git` is absent in current folder | Commit changes with Codex attribution if required |
| Space README links to repo | [DA COMPLETARE] | README has repo placeholder | Add public repo URL |
| Demo video | [DA COMPLETARE] | No video file/link in repo/input | Record 45-60s demo |
| Social post | [DA COMPLETARE] | Draft exists in this file | Publish and add final link if required |
| Gradio app | DONE | `app.py` contains `gr.Blocks` app | None |
| Small model <=32B | DONE | Optional model id: `Qwen/Qwen2.5-3B-Instruct` | None |
| No mandatory cloud API | DONE | README states no required secrets; fallback is local | None |
| Deterministic fallback | DONE | QA passed repeated identical generation | None |
| Safety guard | DONE | `safety_guard()` and blocked patterns implemented | None |
| Track alignment | DONE | README names `An Adventure in Thousand Token Wood` | None |

## Final Ship Plan

| step | owner | output | done criteria | priority |
|---|---|---|---|---|
| 1 | Codex/User | Final README | README includes description, run, safety, model, hackathon fit | P0 |
| 2 | User | Git repository | Public GitHub repo URL | P0 |
| 3 | User | Codex-attributed commits | Commit history satisfies track requirement | P0 |
| 4 | User | Hugging Face Space | Public Space URL opens the Gradio app | P0 |
| 5 | User | Final Space README links | Space README includes GitHub repo link | P0 |
| 6 | User | Final smoke test | Space generates trollsona card and JSON output | P0 |
| 7 | User | Demo video | 45-60s video shows full flow | P1 |
| 8 | User | Social post | Published post with Space and repo placeholders replaced | P1 |
| 9 | User | Submission form | All required links submitted before deadline | P0 |
