# POC

Simple proof of concept for classifying support requests with Google Gemini.

## Setup

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Set `GOOGLE_API_KEY` in `config.py` if you want to call the Gemini API.

## Run

```bash
python main.py
```

## What it does

- Loads sample support messages from `mapping.py`
- Builds a prompt using `prompt.txt`
- Sends the prompt to the Gemini model configured in `config.py`
- Parses the response and prints routing results

## Notes

- `prompt.txt` must exist in the project root.
- `config.py` contains `MODEL_NAME` and `CONFIDENCE_THRESHOLD`.
- This is a lightweight POC, not a production application.
