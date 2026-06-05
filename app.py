from __future__ import annotations

import hashlib
import html
import json
import os
import re
from functools import lru_cache
from typing import Any


APP_TITLE = "Trollsona"
APP_SUBTITLE = "Summon the little menace living behind your respectable personality."
TRACK_NAME = "An Adventure in Thousand Token Wood"
DEFAULT_MODEL_ID = "RthItalia/nano_compact_3b_qkvfp16"
DEFAULT_FALLBACK_MODEL_ID = "Qwen/Qwen2.5-0.5B-Instruct"
MAX_PROFILE_CHARS = 700
MAX_NAME_CHARS = 36


def parse_bool_env(name: str, default: bool) -> bool:
    raw_value = os.getenv(name)
    if raw_value is None:
        return default
    normalized = raw_value.strip().lower()
    if normalized in {"1", "true", "yes", "on"}:
        return True
    if normalized in {"0", "false", "no", "off"}:
        return False
    return default


def parse_int_env(name: str, default: int, min_value: int, max_value: int) -> int:
    raw_value = os.getenv(name)
    if raw_value is None:
        return default
    try:
        value = int(raw_value)
    except ValueError:
        return default
    return max(min_value, min(max_value, value))


MODEL_ID = os.getenv("TROLLSONA_MODEL_ID", DEFAULT_MODEL_ID)
FALLBACK_MODEL_ID = os.getenv("TROLLSONA_FALLBACK_MODEL_ID", DEFAULT_FALLBACK_MODEL_ID)
MODEL_ENABLED = parse_bool_env("TROLLSONA_ENABLE_MODEL", default=False)
MAX_NEW_TOKENS = parse_int_env("TROLLSONA_MAX_NEW_TOKENS", 200, 32, 512)


PERSONA_STYLES = {
    "Back-Alley Oracle": {
        "flavor": "candlelit prophecy from a very suspicious side street",
        "noun_pool": ["Candle", "Omen", "Alley", "Brass", "Whisper", "Ledger"],
    },
    "Basement Prince": {
        "flavor": "royal delusion wrapped in dust, snacks, and old cables",
        "noun_pool": ["Basement", "Velvet", "Outlet", "Throne", "Snack", "Static"],
    },
    "Forest Heckler": {
        "flavor": "mossy woodland sarcasm with a pocket full of bad advice",
        "noun_pool": ["Moss", "Root", "Twig", "Bog", "Fern", "Stump"],
    },
    "Union Goblin": {
        "flavor": "petty workplace grievance with ceremonial clipboard energy",
        "noun_pool": ["Clause", "Mug", "Breakroom", "Badge", "Staple", "Shift"],
    },
    "Dungeon Intern": {
        "flavor": "overworked dungeon bureaucracy and unpaid dramatic labor",
        "noun_pool": ["Ledger", "Torch", "Mop", "Key", "Goblet", "Trapdoor"],
    },
    "Mall Witch": {
        "flavor": "food-court divination with lip gloss and thunder",
        "noun_pool": ["Kiosk", "Charm", "Receipt", "Fountain", "Mascara", "Pretzel"],
    },
    "Parking Lot Philosopher": {
        "flavor": "deep truths delivered beside a dented shopping cart",
        "noun_pool": ["Asphalt", "Cart", "Neon", "Cone", "Puddle", "Keychain"],
    },
    "Saint of Bad Decisions": {
        "flavor": "holy nonsense for people who turn errands into lore",
        "noun_pool": ["Halo", "Candle", "Excuse", "Relic", "Errand", "Confetti"],
    },
    "Meme Caporegime": {
        "flavor": "old-neighborhood swagger filtered through cursed screenshots",
        "noun_pool": ["Pixel", "Prophecy", "Caption", "Scroll", "Vibe", "Echo"],
    },
}

SPICE_LABELS = {
    1: "tiny pinch",
    2: "polite sting",
    3: "back-room heckle",
    4: "crispy little judgment",
    5: "full dossier incident",
}

BLOCKED_PATTERNS = [
    r"\bkill yourself\b",
    r"\bkys\b",
    r"\bself[- ]?harm\b",
    r"\bsuicide\b",
    r"\bhate\b",
    r"\bidiot\b",
    r"\bstupid\b",
    r"\bmoron\b",
    r"\bdumb\b",
    r"\bloser\b",
    r"\bugly\b",
    r"\bworthless\b",
    r"\bsubhuman\b",
    r"\bslur\b",
    r"\bterrorist\b",
    r"\bsexual\b",
    r"\bexplicit\b",
    r"\bprotected class\b",
]

PROTECTED_TARGETING_PATTERNS = [
    r"\bbecause of your race\b",
    r"\bbecause of your religion\b",
    r"\bbecause of your gender\b",
    r"\bbecause of your sexuality\b",
    r"\bbecause of your disability\b",
    r"\bbecause of your nationality\b",
    r"\bbecause of your ethnicity\b",
]

SAFE_REPLY = (
    "The dossier hissed, smoked, and refused to punch down. "
    "Final harmless verdict: your chaos has excellent posture and a suspicious little hat."
)
SAFE_ADVICE = "Make the next useful move before you decorate the excuse."

PRESET_DOSSIERS = [
    {
        "button": "Mira - coffee-built UI oracle",
        "values": (
            "Mira",
            "I overbuild side projects, drink too much coffee, and love weird UI.",
            "Back-Alley Oracle",
            3,
            True,
        ),
    },
    {
        "button": "Alex - label-system dungeon clerk",
        "values": (
            "Alex",
            "I start productivity systems and then reorganize the labels forever.",
            "Dungeon Intern",
            4,
            True,
        ),
    },
    {
        "button": "Sam - tiny-game screenshot boss",
        "values": (
            "Sam",
            "I make tiny games, forget lunch, and name variables like ancient spells.",
            "Meme Caporegime",
            2,
            False,
        ),
    },
]


def stable_int(*parts: str) -> int:
    payload = "||".join(parts).encode("utf-8", errors="ignore")
    return int(hashlib.sha256(payload).hexdigest()[:12], 16)


def clean_text(value: Any, max_chars: int) -> str:
    text = "" if value is None else str(value)
    text = re.sub(r"\s+", " ", text).strip()
    return text[:max_chars]


def clamp_spice(value: Any) -> int:
    try:
        spice = int(value)
    except (TypeError, ValueError):
        spice = 3
    return max(1, min(5, spice))


def compute_cringe_score(profile: str, persona: str, spice: int) -> int:
    base = stable_int(profile.lower(), persona.lower(), str(spice)) % 61
    return max(0, min(100, 22 + base + (spice * 3)))


def cringe_label(score: int) -> str:
    if score < 35:
        return "barely haunted"
    if score < 60:
        return "noticeably cursed"
    if score < 82:
        return "dossier-grade cringe"
    return "full goblin canon event"


def build_prompt(
    user_name: str,
    profile: str,
    persona: str,
    spice: int,
    include_advice: bool,
    score: int,
) -> str:
    style = PERSONA_STYLES.get(persona, PERSONA_STYLES["Forest Heckler"])
    advice_rule = "Include one practical useful_advice sentence." if include_advice else (
        "Set useful_advice to a short note that advice was disabled."
    )
    return f"""
You are Trollsona, a theatrical troll alter-ego generator.
Track: {TRACK_NAME}.

Your job is to transform the user's self-description into a funny, slightly grotesque,
whimsical troll persona. Make it feel like a stained-paper character dossier that was
dictated by a back-alley fortune teller, stamped by a petty clerk, and lightly heckled
by an italo-american cousin who has opinions but not cruelty.

Return only valid minified JSON with these fields:
trollsona_name, troll_reply, useful_advice, cringe_score, cringe_score_label.

Objective:
- Make the result absurd, memorable, specific, and theatrical.
- Make trollsona_name sound like a summoned character, not a username.
- Keep it roasty, not hateful.
- Keep the humor sharp but warm: playful sting, never humiliation.

Style rules:
- Write in vivid, punchy English.
- Use occasional light italo-american flavor, but sparingly.
- Good flavor examples: "listen, paisan", "madone", "capisce".
- Do not overuse slang or turn the voice into a caricature.
- Use grotesque but charming imagery: candle wax, receipts, tiny crowns, haunted binders,
  dented carts, snack dust, side quests, suspicious paperwork.
- No generic roast bot voice.
- No generic assistant copy, no filler, no disclaimers, no moralizing.
- troll_reply must be the strongest comedic line, 1-3 short sentences max.
- useful_advice must contain one real insight in 1 sentence max.

Humor boundaries:
- Roast only habits, vibe, overthinking, productivity rituals, startup energy,
  internet behavior, wording, or harmless personal lore.
- Never attack protected characteristics or identity.
- Never insult appearance, race, ethnicity, religion, disability, nationality,
  gender, sexuality, trauma, mental health, or protected traits.
- Never include threats, self-harm, sexual content, profanity, or slurs.
- Never punch down.

User name: {user_name or "Anonymous traveler"}
User profile: {profile or "No profile supplied."}
Persona: {persona}
Persona flavor: {style["flavor"]}
Spice level: {spice}/5 ({SPICE_LABELS[spice]})
Use this exact deterministic cringe_score: {score}
Use this matching cringe_score_label: {cringe_label(score)}
{advice_rule}
""".strip()


def is_safe_text(text: str) -> bool:
    normalized = text.lower()
    for pattern in BLOCKED_PATTERNS + PROTECTED_TARGETING_PATTERNS:
        if re.search(pattern, normalized):
            return False
    return True


def fallback_trollsona(
    user_name: str,
    profile: str,
    persona: str,
    spice: int,
    include_advice: bool,
    reason: str,
) -> dict[str, Any]:
    style = PERSONA_STYLES.get(persona, PERSONA_STYLES["Forest Heckler"])
    seed = stable_int(user_name.lower(), profile.lower(), persona.lower(), str(spice))
    adjectives = ["Velvet", "Candle", "Ashen", "Brass", "Crooked", "Sainted", "Static"]
    titles = [
        "Overthinker in Residence",
        "Snack Baron of Almost",
        "Dossier Clerk",
        "Chaos Notary",
        "Sidequest Duke",
        "Patron Saint of Later",
    ]
    noun = style["noun_pool"][seed % len(style["noun_pool"])]
    adjective = adjectives[(seed // 7) % len(adjectives)]
    title = titles[(seed // 13) % len(titles)]

    safe_name = re.sub(r"[^A-Za-z0-9 ]+", "", user_name).strip()[:MAX_NAME_CHARS]
    name_prefix = safe_name.title() if safe_name else adjective
    trollsona_name = f"{name_prefix} {noun}-{title}"

    roast_templates = [
        "Listen, paisan: your vibe is a candlelit side quest that opened twelve tabs, found a tiny crown, and called it destiny.",
        "Your aura says main character, but your calendar is dressed like a haunted binder asking for rent.",
        "You are one dramatic cape away from turning a normal errand into a village ordinance.",
        "Your brain is a basement tavern where every idea demands a theme song, a snack bowl, and a separate invoice.",
        "Madone, you carry the confidence of a bridge troll charging tolls in vibes and loose receipts.",
        "You alphabetize chaos, misplace the alphabet, then file a complaint with the moon.",
    ]
    advice_templates = [
        "Pick one task, make it smaller, and finish that version before you rename the kingdom.",
        "Write the next concrete step in one sentence, then do only that step. Capisce?",
        "Keep the weird idea, but give it a deadline and a visible done state.",
        "Trade one dramatic plan for one shipped artifact before the candles burn out.",
        "Use the chaos as seasoning, not as project management.",
    ]

    score = compute_cringe_score(profile, persona, spice)
    reply = roast_templates[(seed // 17 + spice) % len(roast_templates)]
    advice = advice_templates[(seed // 23 + spice) % len(advice_templates)]
    if not include_advice:
        advice = "Truth withheld. The dossier clerk stamps the page and looks away."

    return {
        "trollsona_name": trollsona_name,
        "troll_reply": reply,
        "useful_advice": advice,
        "cringe_score": score,
        "cringe_score_label": cringe_label(score),
        "include_advice": include_advice,
        "runtime": f"model_id={MODEL_ID}; fallback_model_id={FALLBACK_MODEL_ID}; model_enabled={MODEL_ENABLED}",
        "source": "deterministic_fallback",
        "fallback_reason": reason,
    }


@lru_cache(maxsize=1)
def load_model() -> tuple[Any | None, Any | None, str, str]:
    if not MODEL_ENABLED:
        return (
            None,
            None,
            "model disabled by TROLLSONA_ENABLE_MODEL",
            f"model_id={MODEL_ID}; fallback_model_id={FALLBACK_MODEL_ID}; device=disabled",
        )

    try:
        import torch
        from transformers import AutoModelForCausalLM, AutoTokenizer
    except Exception as exc:
        return (
            None,
            None,
            f"model dependencies unavailable: {type(exc).__name__}: {exc}",
            f"model_id={MODEL_ID}; fallback_model_id={FALLBACK_MODEL_ID}; device=unavailable",
        )

    failures: list[str] = []

    def load_tokenizer(candidate_id: str) -> Any:
        tokenizer = AutoTokenizer.from_pretrained(
            candidate_id,
            use_fast=True,
            trust_remote_code=True,
        )
        if tokenizer.pad_token_id is None and tokenizer.eos_token is not None:
            tokenizer.pad_token = tokenizer.eos_token
        return tokenizer

    def load_cuda_model(candidate_id: str) -> Any:
        load_attempts = [
            {
                "trust_remote_code": True,
                "device_map": "cuda",
                "dtype": torch.float16,
                "low_cpu_mem_usage": True,
            },
            {
                "trust_remote_code": True,
                "device_map": "cuda",
                "torch_dtype": torch.float16,
                "low_cpu_mem_usage": True,
            },
            {
                "trust_remote_code": True,
                "torch_dtype": torch.float16,
                "low_cpu_mem_usage": True,
            },
        ]
        last_error: Exception | None = None
        for kwargs in load_attempts:
            try:
                model = AutoModelForCausalLM.from_pretrained(candidate_id, **kwargs)
                if "device_map" not in kwargs:
                    model = model.to("cuda")
                return model
            except Exception as exc:
                last_error = exc
        if last_error is not None:
            raise last_error
        raise RuntimeError("CUDA model load failed without exception")

    def load_cpu_model(candidate_id: str) -> Any:
        try:
            return AutoModelForCausalLM.from_pretrained(
                candidate_id,
                trust_remote_code=True,
                low_cpu_mem_usage=True,
            )
        except TypeError:
            return AutoModelForCausalLM.from_pretrained(candidate_id, trust_remote_code=True)

    candidates = [
        {"role": "primary", "model_id": MODEL_ID, "requires_cuda": True},
        {"role": "fallback_model", "model_id": FALLBACK_MODEL_ID, "requires_cuda": False},
    ]

    seen_model_ids: set[str] = set()
    for candidate in candidates:
        candidate_id = str(candidate["model_id"]).strip()
        if not candidate_id or candidate_id in seen_model_ids:
            continue
        seen_model_ids.add(candidate_id)
        role = str(candidate["role"])
        requires_cuda = bool(candidate["requires_cuda"])

        if requires_cuda and not torch.cuda.is_available():
            failures.append(f"{role} {candidate_id}: CUDA unavailable")
            continue

        try:
            tokenizer = load_tokenizer(candidate_id)
            if torch.cuda.is_available():
                model = load_cuda_model(candidate_id)
                device = "cuda"
            else:
                model = load_cpu_model(candidate_id)
                device = "cpu"
            model.eval()
            torch.manual_seed(0)
            if torch.cuda.is_available():
                torch.cuda.manual_seed_all(0)
            fallback_note = "; ".join(failures)
            status = "model loaded" if not fallback_note else f"model loaded after fallback: {fallback_note}"
            runtime = (
                f"model_id={candidate_id}; role={role}; device={device}; "
                f"cuda_available={torch.cuda.is_available()}"
            )
            return tokenizer, model, status, runtime
        except Exception as exc:
            failures.append(f"{role} {candidate_id}: {type(exc).__name__}: {exc}")

    failure_text = " | ".join(failures) if failures else "no model candidates configured"
    runtime = (
        f"model_id={MODEL_ID}; fallback_model_id={FALLBACK_MODEL_ID}; "
        f"cuda_available={torch.cuda.is_available()}"
    )
    return None, None, f"model load failed: {failure_text}", runtime


def format_generation_prompt(tokenizer: Any, prompt: str) -> str:
    try:
        if getattr(tokenizer, "chat_template", None):
            return tokenizer.apply_chat_template(
                [{"role": "user", "content": prompt}],
                tokenize=False,
                add_generation_prompt=True,
            )
    except Exception:
        return prompt
    return prompt


def generation_temperature(spice: int) -> float:
    return round(0.48 + (clamp_spice(spice) * 0.08), 2)


def model_device(model: Any) -> Any:
    target_device = getattr(model, "device", None)
    if target_device is not None and str(target_device) != "meta":
        return target_device
    try:
        return next(model.parameters()).device
    except Exception:
        return None


def generate_with_model(prompt: str, spice: int) -> tuple[str | None, str, str]:
    tokenizer, model, status, runtime = load_model()
    if tokenizer is None or model is None:
        return None, status, runtime

    try:
        import torch

        model_prompt = format_generation_prompt(tokenizer, prompt)
        inputs = tokenizer(model_prompt, return_tensors="pt", truncation=True, max_length=1536)
        target_device = model_device(model)
        if target_device is not None:
            inputs = {key: value.to(target_device) for key, value in inputs.items()}

        seed = stable_int(prompt, str(spice), runtime) % (2**31)
        torch.manual_seed(seed)
        if hasattr(torch, "cuda") and torch.cuda.is_available():
            torch.cuda.manual_seed_all(seed)

        with torch.no_grad():
            output_ids = model.generate(
                **inputs,
                max_new_tokens=MAX_NEW_TOKENS,
                do_sample=True,
                temperature=generation_temperature(spice),
                num_beams=1,
                repetition_penalty=1.1,
                pad_token_id=tokenizer.eos_token_id,
            )
        prompt_len = inputs["input_ids"].shape[-1]
        generated_ids = output_ids[0][prompt_len:]
        return tokenizer.decode(generated_ids, skip_special_tokens=True).strip(), status, runtime
    except Exception as exc:
        return None, f"model generation failed: {type(exc).__name__}: {exc}", runtime


def parse_loose_model_fields(raw_text: str) -> dict[str, str]:
    fields: dict[str, str] = {}
    for field in ["trollsona_name", "troll_reply", "useful_advice", "cringe_score_label"]:
        pattern = rf'"{field}"\s*:\s*"((?:\\.|[^"\\])*)'
        match = re.search(pattern, raw_text or "", flags=re.DOTALL)
        if not match:
            continue
        try:
            value = json.loads(f'"{match.group(1)}"')
        except json.JSONDecodeError:
            value = match.group(1)
        fields[field] = str(value)
    return fields


def coerce_model_result(
    parsed: dict[str, Any],
    fallback: dict[str, Any],
    score: int,
    include_advice: bool,
    fallback_reason: str,
    runtime: str,
) -> dict[str, Any] | None:
    result = dict(fallback)
    field_limits = {
        "trollsona_name": 80,
        "troll_reply": 360,
        "useful_advice": 280,
        "cringe_score_label": 80,
    }
    used_fields: list[str] = []
    missing_fields: list[str] = []

    for field, limit in field_limits.items():
        value = clean_text(parsed.get(field), limit)
        if value and is_safe_text(value):
            result[field] = value
            used_fields.append(field)
        else:
            missing_fields.append(field)

    if not used_fields:
        return None

    result["cringe_score"] = score
    result["include_advice"] = include_advice
    result["source"] = "transformers_model"
    result["runtime"] = runtime
    if missing_fields:
        partial_reason = f"model output partial; fallback filled: {', '.join(missing_fields)}"
        result["fallback_reason"] = (
            f"{fallback_reason}; {partial_reason}" if fallback_reason else partial_reason
        )
    else:
        result["fallback_reason"] = fallback_reason
    return result


def parse_model_output(
    raw_text: str,
    fallback: dict[str, Any],
    score: int,
    include_advice: bool,
    fallback_reason: str,
    runtime: str,
) -> dict[str, Any] | None:
    decoder = json.JSONDecoder()
    parsed = None
    for match in re.finditer(r"\{", raw_text or ""):
        try:
            candidate, _ = decoder.raw_decode(raw_text[match.start() :])
        except json.JSONDecodeError:
            continue
        if isinstance(candidate, dict):
            parsed = candidate
            break

    if parsed is None:
        parsed = parse_loose_model_fields(raw_text)

    return coerce_model_result(parsed, fallback, score, include_advice, fallback_reason, runtime)


def repair_model_output(
    raw_text: str,
    fallback: dict[str, Any],
    fallback_reason: str,
    runtime: str,
) -> dict[str, Any] | None:
    repaired_reply = clean_text(raw_text, 360)
    repaired_reply = re.sub(r"^```(?:json)?|```$", "", repaired_reply).strip()
    if not repaired_reply or repaired_reply.startswith("{"):
        return None
    if not is_safe_text(repaired_reply):
        return None

    result = dict(fallback)
    result["troll_reply"] = repaired_reply
    result["source"] = "transformers_model_repaired"
    result["runtime"] = runtime
    repair_reason = "model output was not valid JSON and was repaired"
    result["fallback_reason"] = f"{fallback_reason}; {repair_reason}" if fallback_reason else repair_reason
    return result


def safety_guard(result: dict[str, Any], fallback: dict[str, Any]) -> dict[str, Any]:
    fields = [
        result.get("trollsona_name", ""),
        result.get("troll_reply", ""),
        result.get("useful_advice", ""),
        result.get("cringe_score_label", ""),
    ]
    if not all(is_safe_text(str(field)) for field in fields):
        guarded = dict(fallback)
        guarded["troll_reply"] = SAFE_REPLY
        guarded["useful_advice"] = SAFE_ADVICE
        guarded["fallback_reason"] = "safety guard replaced unsafe output"
        return guarded
    return result


def render_card(result: dict[str, Any]) -> str:
    esc = {key: html.escape(str(value)) for key, value in result.items()}
    score = max(0, min(100, int(result.get("cringe_score", 0))))
    useful_advice = clean_text(result.get("useful_advice", ""), 280)
    show_advice = bool(result.get("include_advice", True)) and bool(useful_advice)
    advice_tile = (
        f"""
    <div class="trollsona-tile">
      <div class="trollsona-label">A USEFUL SLAP</div>
      <div class="trollsona-value">{html.escape(useful_advice)}</div>
    </div>
""".rstrip()
        if show_advice
        else ""
    )
    grid_class = "trollsona-grid" if show_advice else "trollsona-grid trollsona-grid-single"
    return f"""
<div class="trollsona-card">
  <div class="dossier-kicker">THE SUMMONED MENACE</div>
  <h2>{esc["trollsona_name"]}</h2>
  <div class="trollsona-mainline">{esc["troll_reply"]}</div>
  <div class="{grid_class}">
{advice_tile}
    <div class="trollsona-tile">
      <div class="trollsona-label">GOBLIN METER</div>
      <div class="meter-shell" aria-label="Goblin meter {score} out of 100">
        <div class="meter-fill" style="width: {score}%"></div>
      </div>
      <div class="trollsona-value">{score}/100 - {esc["cringe_score_label"]}</div>
    </div>
  </div>
</div>
""".strip()


def render_cursed_paperwork(result: dict[str, Any]) -> str:
    source = clean_text(result.get("source", "unknown"), 80)
    runtime = clean_text(result.get("runtime", "runtime unavailable"), 260)
    fallback_reason = clean_text(result.get("fallback_reason", ""), 180)
    if not fallback_reason:
        fallback_reason = "No fallback note."
    return (
        f"**Source:** `{source}`  \n"
        f"**Runtime:** `{runtime}`  \n"
        f"**Fallback note:** {fallback_reason}"
    )


def render_empty_card() -> str:
    return """
<div class="empty-dossier">
  <div class="dossier-kicker">The dossier is sealed</div>
  <h2>No menace has signed the paperwork yet.</h2>
  <p>Feed the booth a little lore, pick a resident menace, and pull the handle.</p>
</div>
""".strip()


def load_preset(index: int) -> tuple[str, str, str, int, bool]:
    return PRESET_DOSSIERS[index]["values"]


def generate_trollsona(
    user_name: str,
    profile: str,
    persona: str,
    spice: int,
    include_advice: bool,
) -> tuple[str, dict[str, Any], str]:
    user_name = clean_text(user_name, MAX_NAME_CHARS)
    profile = clean_text(profile, MAX_PROFILE_CHARS)
    persona = persona if persona in PERSONA_STYLES else "Forest Heckler"
    spice = clamp_spice(spice)
    include_advice = bool(include_advice)

    fallback = fallback_trollsona(
        user_name=user_name,
        profile=profile,
        persona=persona,
        spice=spice,
        include_advice=include_advice,
        reason="model unavailable or output invalid",
    )

    score = compute_cringe_score(profile, persona, spice)
    prompt = build_prompt(user_name, profile, persona, spice, include_advice, score)
    raw_text, model_status, runtime = generate_with_model(prompt, spice)
    model_fallback_reason = "" if model_status == "model loaded" else model_status

    result = None
    if raw_text:
        result = parse_model_output(
            raw_text=raw_text,
            fallback=fallback,
            score=score,
            include_advice=include_advice,
            fallback_reason=model_fallback_reason,
            runtime=runtime,
        )
        if result is None:
            result = repair_model_output(raw_text, fallback, model_fallback_reason, runtime)

    if result is None:
        result = dict(fallback)
        result["fallback_reason"] = model_status
        result["runtime"] = runtime

    result = safety_guard(result, fallback)
    return render_card(result), result, render_cursed_paperwork(result)


def build_demo() -> Any:
    import gradio as gr

    css = ""
    css_path = os.path.join(os.path.dirname(__file__), "assets", "style.css")
    if os.path.exists(css_path):
        with open(css_path, "r", encoding="utf-8") as handle:
            css = handle.read()

    with gr.Blocks(title=APP_TITLE, css=css) as demo:
        gr.HTML(
            f"""
<section class="ritual-hero">
  <div class="hero-mark">Trollsona</div>
  <h1>{APP_TITLE}</h1>
  <p>{APP_SUBTITLE}</p>
  <div class="badge-row">
    <span>Build Small Hackathon</span>
    <span>Small model</span>
    <span>Safe grotesque humor</span>
    <span>{TRACK_NAME}</span>
  </div>
</section>
""".strip()
        )

        with gr.Row(elem_classes=["ritual-layout"]):
            with gr.Column(scale=1, elem_classes=["summoning-panel"]):
                gr.HTML('<div class="panel-heading">The summoning booth</div>')
                user_name = gr.Textbox(
                    label="What do they call you?",
                    placeholder="Mira",
                    max_lines=1,
                )
                profile = gr.Textbox(
                    label="Confess your little lore",
                    placeholder="I overbuild side projects, drink too much coffee, and love weird UI.",
                    lines=5,
                    max_lines=7,
                )
                persona = gr.Dropdown(
                    label="Pick your resident menace",
                    choices=list(PERSONA_STYLES.keys()),
                    value="Back-Alley Oracle",
                )
                spice = gr.Slider(
                    label="How hard should it sting?",
                    minimum=1,
                    maximum=5,
                    value=3,
                    step=1,
                )
                include_advice = gr.Checkbox(label="Slip in one useful truth", value=True)
                generate_button = gr.Button("Summon Trollsona", variant="primary")

            with gr.Column(scale=1, elem_classes=["dossier-stage"]):
                card_output = gr.HTML(value=render_empty_card())
                debug_state = gr.State()
                with gr.Accordion("See the cursed paperwork", open=False):
                    debug_output = gr.Markdown(
                        value=(
                            "**Source:** `not summoned`  \n"
                            "**Runtime:** `not summoned`  \n"
                            "**Fallback note:** The dossier clerk is still asleep."
                        )
                    )

        generate_button.click(
            fn=generate_trollsona,
            inputs=[user_name, profile, persona, spice, include_advice],
            outputs=[card_output, debug_state, debug_output],
        )

        with gr.Accordion("Stolen dossiers", open=False):
            gr.HTML('<div class="preset-note">Tap a stolen dossier to pre-fill the booth.</div>')
            with gr.Row(elem_classes=["preset-row"]):
                for preset_index, preset in enumerate(PRESET_DOSSIERS):
                    preset_button = gr.Button(
                        preset["button"],
                        variant="secondary",
                        elem_classes=["preset-card"],
                    )
                    preset_button.click(
                        fn=lambda index=preset_index: load_preset(index),
                        inputs=[],
                        outputs=[user_name, profile, persona, spice, include_advice],
                    )

    return demo


demo = None if parse_bool_env("TROLLSONA_SKIP_UI_BUILD", default=False) else build_demo()


if __name__ == "__main__":
    (demo or build_demo()).launch()
