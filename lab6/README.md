# Задача 25: Генератор QR-payload для пропуска на мероприятие

**Студент:** Сидоркевич А.В.

**Постановка задачи:** Формирование строки payload (id, timestamp, подпись-заглушка) и её разбор. Тесты round-trip. Пайплайн + Pages с описанием формата.

## Структура проекта
- `qr_payload.py` — код (сборка и разбор payload).
- `test_qr_payload.py` — тесты.
- `generate_docs.py` — скрипт для создания HTML-страницы.
- `.github/workflows/ci.yml` — CI/CD пайплайн.

## Запуск тестов локально
```bash
pip install -r requirements.txt
pytest -q