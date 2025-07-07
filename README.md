# DeepSolver

This script automatically captures screen text (e.g., test questions) and uses AI to find correct answers.

## Features

- Screen capture with hotkey
- Text recognition using Tesseract OCR
- Question analysis and answer generation using DeepSeek AI via OpenRouter API
- Console output of answers

## Installation

1. Install dependencies:
```bash
pip install pillow pytesseract keyboard requests
```

2. Install Tesseract OCR:
- Download from [official github](https://github.com/UB-Mannheim/tesseract/wiki)
- Set path in `TESSERACT_PATH` variable

3. Get API key from [OpenRouter](https://openrouter.ai/) and set it in `OPENROUTER_API_KEY`

## 🎮 Usage

1. Run the script:
```bash
python deepsolve.py
```

2. Open your test or questionnaire
3. Press `Num 4` (or your configured hotkey) to process screenshot
4. Receive answer in console

## Configuration

You can modify:
- Hotkey (`HOTKEY`)
- AI model (`model` in `ask_deepseek` function)
- Image processing parameters (in `image_to_text` function)

API responses are saved to `debug.json` for debugging.
