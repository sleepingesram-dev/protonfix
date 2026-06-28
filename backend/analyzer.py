import os
import json
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


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
    prompt = f"""
You are ProtonFix AI, a Linux gaming troubleshooting assistant.

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

    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {"role": "user", "content": prompt}
        ],
        temperature=0.1,
    )

    raw_text = response.choices[0].message.content
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
