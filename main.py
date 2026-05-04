import tkinter as tk
from tkinter import ttk, messagebox
import random
import string
import json
import pyperclip
import os

CONFIG_FILE = "history.json"

def load_history():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

def save_history(data):
    with open(CONFIG_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def generate_password(length, use_digits, use_letters, use_symbols):
    chars = ''
    if use_digits: chars += string.digits
    if use_letters: chars += string.ascii_letters
    if use_symbols: chars += string.punctuation
    if not chars:
        raise ValueError('Не выбран ни один тип символов!')
    return ''.join(random.choices(chars, k=length))

def on_generate():
    try:
        length = int(length_var.get())
        if length < 4 or length > 50:
            messagebox.showwarning("Ошибка", "Длина пароля должна быть от 4 до 50 символов.")
            return
    except ValueError:
        messagebox.showwarning("Ошибка", "Длина пароля должна быть числом.")
        return

    use_digits = var_digits.get()
    use_letters = var_letters.get()
    use_symbols = var_symbols.get()

    if not (use_digits or use_letters or use_symbols):
        messagebox.showwarning("Ошибка", "Выберите хотя бы один тип символов.")
        return

    try:
        password = generate_password(length, use_digits, use_letters, use_symbols)
        password_entry.delete(0, tk.END)
        password_entry.insert(0, password)

        history.append(password)
        save_history(history)
        update_history_table()
    except Exception as e:
        messagebox.showerror("Ошибка", str(e))

def copy_to_clipboard():
    password = password_entry.get()
    if password:
        pyperclip.copy(password)

def clear_history():
    if messagebox.askyesno("Подтвердите", "Очистить всю историю?"):
        global history
        history = []
        save_history(history)
        update_history_table()

def update_history_table():
    for i in history_table.get_children():
        history_table.delete(i)
    for p in history:
        history_table.insert("", tk.END, values=(p,))

# --- Основное окно ---
root = tk.Tk()
root.title("Генератор случайных паролей")
root.geometry("600x500")

# --- Переменные ---
length_var = tk.StringVar(value="12")
var_digits = tk.BooleanVar(value=True)
var_letters = tk.BooleanVar(value=True)
var_symbols = tk.BooleanVar(value=True)

# --- Ввод ---
frame_settings = ttk.LabelFrame(root, text="Настройки", padding=10)
frame_settings.pack(fill="x", padx=10, pady=5)

ttk.Label(frame_settings, text="Длина пароля:").grid(row=0, column=0, sticky="w")
length_entry = ttk.Entry(frame_settings, textvariable=length_var, width=10)
length_entry.grid(row=0, column=1, padx=5)

ttk.Checkbutton(frame_settings, text="Цифры", variable=var_digits).grid(row=1, column=0, sticky="w")
ttk.Checkbutton(frame_settings, text="Буквы", variable=var_letters).grid(row=1, column=1, sticky="w")
ttk.Checkbutton(frame_settings, text="Спецсимволы", variable=var_symbols).grid(row=1, column=2, sticky="w")

ttk.Button(frame_settings, text="Сгенерировать", command=on_generate).grid(row=2, column=0, columnspan=3, pady=10)

# --- Результат ---
frame_result = ttk.Frame(root, padding=10)
frame_result.pack(fill="x", padx=10, pady=5)

ttk.Label(frame_result, text="Сгенерированный пароль:").pack(anchor="w")
password_entry = ttk.Entry(frame_result, width=50)
password_entry.pack(pady=5)
ttk.Button(frame_result, text="Копировать", command=copy_to_clipboard).pack(pady=5)

# --- История ---
frame_history = ttk.LabelFrame(root, text="История", padding=10)
frame_history.pack(fill="both", expand=True, padx=10, pady=5)

history_table = ttk.Treeview(frame_history, columns=("password",), show="headings")
history_table.heading("password", text="Пароль")
history_table.column("password", minwidth=200, width=400)
history_table.pack(fill="both", expand=True)

ttk.Button(frame_history, text="Очистить историю", command=clear_history).pack(pady=5)

# --- Загрузка истории ---
history = load_history()
update_history_table()

root.mainloop()