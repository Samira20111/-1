import tkinter as tk
from tkinter import ttk, messagebox
import random
import string
import json
import os

# --- Настройки ---
HISTORY_FILE = 'password_history.json'
MIN_LENGTH = 4
MAX_LENGTH = 32

# --- Функции логики ---
def load_history():
    """Загружает историю паролей из файла JSON."""
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return []

def save_history(history):
    """Сохраняет историю паролей в файл JSON."""
    with open(HISTORY_FILE, 'w', encoding='utf-8') as f:
        json.dump(history, f, ensure_ascii=False, indent=2)

def generate_password():
    """Генерирует пароль на основе выбранных параметров."""
    length = length_var.get()
    
    # Проверка длины
    if length < MIN_LENGTH or length > MAX_LENGTH:
        messagebox.showwarning("Ошибка", f"Длина пароля должна быть от {MIN_LENGTH} до {MAX_LENGTH} символов.")
        return

    # Сбор символов для генерации
    chars = ''
    if use_digits.get(): chars += string.digits
    if use_letters.get(): chars += string.ascii_lowercase
    if use_upper.get(): chars += string.ascii_uppercase
    if use_special.get(): chars += string.punctuation

    if not chars:
        messagebox.showwarning("Ошибка", "Выберите хотя бы один тип символов.")
        return

    # Генерация пароля
    password = ''.join(random.choices(chars, k=length))
    
    # Отображение и сохранение в историю
    password_entry.delete(0, tk.END)
    password_entry.insert(0, password)
    
    history.append(password)
    save_history(history)
    update_history_table()

def update_history_table():
    """Обновляет таблицу истории в GUI."""
    for i in history_table.get_children():
        history_table.delete(i)
    for pwd in history:
        history_table.insert('', 'end', values=(pwd,))

def clear_history():
    """Очищает историю паролей."""
    if messagebox.askyesno("Очистить историю", "Вы уверены, что хотите удалить всю историю?"):
        global history
        history = []
        save_history(history)
        update_history_table()

# --- Инициализация данных ---
history = load_history()

# --- Создание окна ---
root = tk.Tk()
root.title("Генератор случайных паролей")
root.geometry("600x450")
root.resizable(False, False)

# --- Фрейм настроек ---
settings_frame = tk.LabelFrame(root, text="Настройки", padx=10, pady=10)
settings_frame.pack(pady=10, fill='x')

# Длина пароля
tk.Label(settings_frame, text="Длина пароля:").grid(row=0, column=0, sticky='w')
length_var = tk.IntVar(value=12)
length_slider = tk.Scale(settings_frame, from_=MIN_LENGTH, to=MAX_LENGTH, orient='horizontal', variable=length_var)
length_slider.grid(row=0, column=1, columnspan=2, sticky='ew')

# Чекбоксы символов
use_digits = tk.BooleanVar(value=True)
use_letters = tk.BooleanVar(value=True)
use_upper = tk.BooleanVar(value=True)
use_special = tk.BooleanVar(value=True)

tk.Checkbutton(settings_frame, text="Цифры (0-9)", variable=use_digits).grid(row=1, column=0, sticky='w')
tk.Checkbutton(settings_frame, text="Строчные буквы (a-z)", variable=use_letters).grid(row=2, column=0, sticky='w')
tk.Checkbutton(settings_frame, text="Заглавные буквы (A-Z)", variable=use_upper).grid(row=1, column=1, sticky='w')
tk.Checkbutton(settings_frame, text="Спецсимволы (!@#$)", variable=use_special).grid(row=2, column=1, sticky='w')

# Кнопка генерации
gen_button = tk.Button(root, text="Сгенерировать пароль", command=generate_password)
gen_button.pack(pady=5)

# Поле для вывода пароля
password_entry = tk.Entry(root, font=('Consolas', 14), width=40)
password_entry.pack(pady=5)
password_entry.insert(0, "Здесь появится ваш пароль")

# Фрейм истории
history_frame = tk.LabelFrame(root, text="История паролей", padx=5, pady=5)
history_frame.pack(pady=10, fill='both', expand=True)

# Таблица истории (Treeview)
history_table = ttk.Treeview(history_frame, columns=("password",), show="headings")
history_table.heading("password", text="Пароль")
history_table.column("password", width=500)
history_table.pack(fill='both', expand=True)

# Кнопка очистки истории
clear_button = tk.Button(history_frame, text="Очистить историю", command=clear_history)
clear_button.pack(pady=5)

# Обновляем таблицу при запуске
update_history_table()

# Запуск приложения
root.mainloop()