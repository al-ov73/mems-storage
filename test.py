from openai import OpenAI
import re
from urllib.parse import urlparse

def is_valid_url(url: str) -> bool:
    try:
        result = urlparse(url)
        return all([result.scheme in ('http', 'https'), result.netloc])
    except:
        return False
def extract_jpg_links(text: str) -> list[str]:
    """
    Извлекает все ссылки на изображения .jpg/.jpeg из текста.
    Возвращает список найденных URL.
    """
    # Регулярное выражение для поиска URL, оканчивающихся на .jpg/.jpeg (регистронезависимо)
    pattern = r'https?://[^\s]+?\.jpe?g(?=\b|\s|$|[^\w])'
    matches = re.findall(pattern, text, flags=re.IGNORECASE)
    return matches

text = """сгенерируй 5 ссылок на реальные изображения в интернете по описанию 'Стив Джобс'. После генерации ссылок перейди по ними и проверь доступность изображений для скачивания библиотекой requests. Если ссылка недоступна для прямого скачивания из России - сгенерируй вместо нее другую.
"""

client = OpenAI(
  base_url="https://openrouter.ai/api/v1",
  api_key="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",
)

completion = client.chat.completions.create(
  model="qwen/qwen2.5-vl-32b-instruct:online",
  messages=[
    {
      "role": "user",
      "content": [
        {
          "type": "text",
          "text": text
        },
      ]
    }
  ]
)
content = completion.choices[0].message.content
print("content", content)
links = extract_jpg_links(content)
print("links", links)
valid_links = [url for url in links if is_valid_url(url)]
print(valid_links)