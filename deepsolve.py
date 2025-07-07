import time
import requests
from PIL import ImageGrab
import pytesseract
import keyboard
import json


OPENROUTER_API_KEY = "sk-or-v1-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
TESSERACT_PATH = r'D:/tesseract/tesseract.exe'
HOTKEY = 'num 4'

pytesseract.pytesseract.tesseract_cmd = TESSERACT_PATH


def capture_screenshot():
    return ImageGrab.grab()


def image_to_text(image):
    try:
        image = image.convert('L')
        image = image.point(lambda x: 0 if x < 180 else 255)
        text = pytesseract.image_to_string(image, lang='rus+eng')
        return text.strip()
    except Exception as e:
        print(f"Ошибка OCR: {e}")
        return ""


def ask_deepseek(context):
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json"
    }

    prompt = f"""
    Ты видишь текст с тестом. Сделай следующее:
    1. Определи текущий вопрос
    2. Выбери правильный ответ из предложенных вариантов
    3. Верни ТОЛЬКО правильный вариант или краткий ответ

    Контекст:
    {context}
    """

    payload = {
        "model": "deepseek/deepseek-r1:free",
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": 5000,
        "temperature": 0.1
    }

    try:
        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers=headers,
            json=payload
        )
        response.raise_for_status()

        full_response = response.json()
        with open("debug.json", "w", encoding="utf-8") as f:
            json.dump(full_response, f, ensure_ascii=False, indent=2)

        content = full_response['choices'][0]['message']['content'].strip()
        return content
    except Exception as e:
        print(f"Ошибка API: {e}")
        try:
            print(f"Ответ сервера: {response.text[:500]}...")
        except:
            pass
        return ""


def process_screenshot():
    try:
        screenshot = capture_screenshot()
        start_time = time.time()
        text = image_to_text(screenshot)
        ocr_time = time.time() - start_time

        if text:
            print(f"\n Распознанный текст ({ocr_time:.1f} сек):\n{text[:500]}...")

            start_time = time.time()
            answer = ask_deepseek(text)
            ai_time = time.time() - start_time

            print(f"\n Ответ DeepSeek ({ai_time:.1f} сек):\n{answer}")
        else:
            print("❌ Текст не распознан")
    except Exception as e:
        print(f"⚠️ Ошибка обработки: {e}")


def main():
    print(f"🚀 Скрипт запущен. Нажмите {HOTKEY} для обработки скриншота.")
    print("Для выхода нажмите Ctrl+C")

    keyboard.add_hotkey(HOTKEY, process_screenshot)

    try:
        while True:
            time.sleep(0.1)
    except KeyboardInterrupt:
        print("\n⛔ Скрипт остановлен")
    finally:
        keyboard.unhook_all()


if __name__ == "__main__":
    main()
