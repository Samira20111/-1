# Random Password Generator

**Автор:** Миннегалиева Самира 
**Вариант:** "Random Password Generator"
**Дата:** май 2026

## Описание

Графическое приложение для генерации случайных паролей с настройкой параметров и сохранением истории. Реализовано на Python с использованием customtkinter.

## Установка

1. Клонируйте репозиторий:
   ```bash
   git clone https://github.com/ваш_логин/Random-Password-Generator.git
   cd Random-Password-Generator
   ```
2. Создайте виртуальное окружение:
   ```bash
   python -m venv venv
   source venv/bin/activate  # Для Windows: venv\Scripts\activate
   ```
3. Установите зависимости:
   ```bash
   pip install -r requirements.txt
   ```
4. Запустите приложение:
   ```bash
   python main.py
   ```

## Использование

- Задайте длину пароля ползунком.
- Выберите типы символов чекбоксами.
- Нажмите «Сгенерировать» — пароль появится в поле и добавится в историю.
- История сохраняется в `history.json`.