> [!NOTE]\
> Данный веб-сайт никак не связан с Корпорацией Microsoft, все права на торговую марку Windows© пренадлежат Корпорации Microsoft

# Windows81Online

**Веб-сайт в стиле Windows 8.1 с функционалом бота в Telegram @basster284sbot**

## Возможности

- Магазин модов Geode

## Как задеплоить

1. Установить Python выше 3.13.9
2. Установить библиотеки из `requirements.txt`
3. Создать файл с именем `wsgi.py` и записать в нём следующие строки:
```python
from app import app

if __name__ == "__main__":
    app.run()
```
4. В терминале ввести следующее:
```bash
gunicorn --workers 1 --bind 127.0.0.1:8000 wsgi:app
```