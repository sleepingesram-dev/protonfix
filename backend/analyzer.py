import os
import json
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

_client: OpenAI | None = None


def _get_client() -> OpenAI | None:
    """Create the OpenAI client lazily so the app can start (and the
    deterministic engine can run) without an API key configured."""
    global _client
    if _client is None and os.getenv("OPENAI_API_KEY"):
        _client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    return _client


def _unavailable_diagnosis(reason: str) -> dict:
    return {
        "summary": "No known error pattern matched this log, and the AI fallback is unavailable.",
        "probable_cause": reason,
        "confidence": "low",
        "severity": "low",
        "detected_errors": [],
        "fix_steps": [
            "Check the log manually for error lines (err:, VK_ERROR, failed).",
            "Try a different Proton version.",
            "Verify game files in Steam.",
        ],
        "recommended_commands": [],
        "extra_info_needed": [],
        "warnings": [
            "This log did not match any known fingerprint. The AI-based analysis "
            "could not run, so no automated diagnosis is available."
        ],
    }


def clean_json_response(text: str) -> str:
    text = text.strip()

    if text.startswith("```json"):
        text = text.replace("```json", "", 1).strip()

    if text.startswith("```"):
        text = text.replace("```", "", 1).strip()

    if text.endswith("```"):
        text = text[:-3].strip()

    return text


def analyze_log_text(log_text: str, parsed: dict) -> dict:
    client = _get_client()
    if client is None:
        return _unavailable_diagnosis(
            "OPENAI_API_KEY is not configured on the server, so the AI fallback is disabled."
        )

    prompt = f"""
You are ProtonFix, a Linux gaming troubleshooting assistant.

Analyze the uploaded Steam, Proton, Wine, DXVK, VKD3D, Gamescope, GameMode, or GPU driver log.

Return ONLY valid JSON.
Do not use markdown.
Do not wrap the response in triple backticks.

Use this exact JSON format:

{{
  "summary": "",
  "probable_cause": "",
  "confidence": "low | medium | high",
  "severity": "low | medium | high",
  "detected_errors": [],
  "fix_steps": [],
  "recommended_commands": [],
  "extra_info_needed": [],
  "warnings": []
}}

Rules:
- Be practical.
- Do not guess beyond the log.
- If the log is fake or incomplete, say what is missing.
- Fix steps should be beginner-friendly.
- Mention Linux commands only when useful.
- Keep the answer focused on gaming troubleshooting.
- Use the parsed log data first.
- Use the raw log excerpt only as supporting evidence.
- Do not recommend unsafe commands like rm -rf, chmod -R 777, or running Steam as root.

Parsed log data:
{json.dumps(parsed, indent=2)}

Raw log excerpt:
{log_text[:12000]}
"""

    try:
        response = client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=[
                {"role": "user", "content": prompt}
            ],
            temperature=0.1,
        )
    except Exception as exc:
        return _unavailable_diagnosis(f"The AI analysis request failed: {exc}")

    raw_text = response.choices[0].message.content or ""
    cleaned_text = clean_json_response(raw_text)

    try:
        return json.loads(cleaned_text)
    except json.JSONDecodeError:
        return {
            "summary": "AI responded, but the response could not be parsed as JSON.",
            "probable_cause": "JSON parsing failed.",
            "confidence": "low",
            "severity": "medium",
            "detected_errors": [],
            "fix_steps": [
                "Try uploading the log again.",
                "If this keeps happening, the AI response format needs adjustment."
            ],
            "recommended_commands": [],
            "extra_info_needed": [],
            "warnings": [raw_text]
        }
