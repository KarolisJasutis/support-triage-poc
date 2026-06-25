import json
from typing import Any, Dict, List

import google.generativeai as genai

from config import CONFIDENCE_THRESHOLD, GOOGLE_API_KEY, MODEL_NAME
from mapping import SAMPLE_SUPPORT_MESSAGES, TEAM_CATEGORIES


def build_category_team_section(categories: Dict[str, List[str]]) -> str:
    """Build a readable category/team section for the prompt."""
    lines: List[str] = []
    for team_name, category_keys in categories.items():
        lines.append(f"{team_name}:")
        for category_key in category_keys:
            lines.append(f"* {category_key}")
        lines.append("")
    return "\n".join(lines).strip()


def extract_json_from_text(text: str):
    """Extract the first JSON object found in the model response text."""
    start_index = text.find("{")
    if start_index == -1:
        return None

    brace_depth = 0
    in_string = False
    escape = False

    for index in range(start_index, len(text)):
        char = text[index]

        if in_string:
            if escape:
                escape = False
            elif char == "\\":
                escape = True
            elif char == '"':
                in_string = False
        else:
            if char == '"':
                in_string = True
            elif char == "{":
                brace_depth += 1
            elif char == "}":
                brace_depth -= 1
                if brace_depth == 0:
                    return text[start_index : index + 1]
    return None


def parse_model_response(response_text: str) -> Dict[str, Any]:
    """Parse the model response and return a normalized result dictionary."""
    parsed: Dict[str, Any] = {
        "category": "",
        "team": "",
        "confidence": 0.0,
        "reason": "",
        "clarification_questions": []
    }

    json_text = extract_json_from_text(response_text)
    if not json_text:
        parsed["reason"] = "Could not locate JSON object in model response."
        return parsed

    try:
        data = json.loads(json_text)
    except json.JSONDecodeError as exc:
        parsed["reason"] = f"Failed to parse JSON: {exc}"  # type: ignore[assignment]
        return parsed

    if isinstance(data, dict):
        parsed["category"] = str(data.get("category", ""))
        parsed["team"] = str(data.get("team", ""))

        confidence_value = data.get("confidence", 0.0)
        try:
            parsed["confidence"] = float(confidence_value)
        except (TypeError, ValueError):
            parsed["confidence"] = 0.0

        parsed["reason"] = str(data.get("reason", ""))

        clarification = data.get("clarification_questions", [])
        if isinstance(clarification, list):
            parsed["clarification_questions"] = [str(item) for item in clarification]
        else:
            parsed["clarification_questions"] = [str(clarification)]
    else:
        parsed["reason"] = "JSON parsed but did not contain an object."

    return parsed


def format_clarification_questions(questions: List[str]) -> str:
    """Format clarification questions for console output."""
    if not questions:
        return "None"
    return "\n".join(f"* {question}" for question in questions)


def format_output(message: str, result: Dict[str, Any]) -> str:
    """Format the final routing result for console display."""
    status = "AUTO ROUTE" if result["confidence"] > CONFIDENCE_THRESHOLD else "MANUAL REVIEW"
    clarification_text = format_clarification_questions(result["clarification_questions"])

    return (
        "=" * 50
        + "\n"
        + "SUPPORT MESSAGE\n"
        + f"{message}\n\n"
        + f"Predicted Team: {result['team']}\n"
        + f"Category: {result['category']}\n"
        + f"Confidence: {result['confidence']:.2f}\n\n"
        + f"Status: {status}\n\n"
        + f"Reason: {result['reason']}\n\n"
        + "Clarification Questions:\n"
        + f"{clarification_text}\n"
        + "=" * 50
    )


def main() -> None:
    """Run the support request classification workflow for sample messages."""
    genai.configure(api_key=GOOGLE_API_KEY)
    model = genai.GenerativeModel(MODEL_NAME)

    category_team_section = build_category_team_section(TEAM_CATEGORIES)

    try:
        with open("prompt.txt", "r", encoding="utf-8") as prompt_file:
            prompt_template = prompt_file.read()
    except FileNotFoundError:
        print("Error: prompt.txt not found.")
        return

    for support_message in SAMPLE_SUPPORT_MESSAGES:
        prompt = prompt_template.replace("{CATEGORIES_AND_TEAMS}", category_team_section)
        prompt = prompt.replace("{SUPPORT_REQUEST}", support_message)

        try:
            response = model.generate_content(prompt)
            response_text = response.text
        except Exception as exc:
            error_result = {
                "category": "",
                "team": "",
                "confidence": 0.0,
                "reason": f"Gemini request failed: {exc}",
                "clarification_questions": []
            }
            print(format_output(support_message, error_result))
            continue

        result = parse_model_response(response_text)
        print(format_output(support_message, result))


if __name__ == "__main__":
    main()
