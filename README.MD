# Async HTTP Client with Proxy Support

Асинхронный HTTP клиент с поддержкой прокси и управлением сессиями

## Особенности

- 🚀 Асинхронные HTTP запросы с помощью aiohttp
- 🔒 Поддержка прокси с авторизацией
- 📦 Упрощенное управление сессиями
- 🎲 Рандомизация прокси из файла
- 📄 Поддержка форматов ответов JSON и TEXT
- ⚙️ Гибкая настройка заголовков и параметров

## Требования

- Python 3.11+ (минимальная тестированная версия)
- Пакетный менеджер pip

## Установка

1. Создайте виртуальное окружение:
```bash
python -m venv venv
source venv/bin/activate  # Linux/MacOS
venv\Scripts\activate.bat  # Windows
```

2. Установите зависимости:
```bash
pip install -r requirements.txt
```

### Формат файла прокси
- Создайте в корне проекта файл `proxies.txt`.
- Файл `proxies.txt` должен содержать прокси в формате:
```
http://host:port:login:password
socks5://127.0.0.1:8080:user:pass
```

### Основные методы
```python
# Инициализация клиента
client = AsyncHttpClient()

# Выполнение запроса
await client.fetch(
    url="https://example.com",
    method="GET",
    mode="JSON",
    headers={"User-Agent": "MyBot"},
    params={"page": 2}
)

# Закрытие сессии
await client.close()
```

## Лучшие практики
1. Всегда используйте контекстный менеджер (`async with`)
2. Проверяйте доступность прокси перед использованием
3. Обрабатывайте исключения для сетевых ошибок
4. Используйте разные User-Agent для запросов
