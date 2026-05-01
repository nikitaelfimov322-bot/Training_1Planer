import tkinter as tk
from tkinter import ttk, messagebox
import json
from datetime import datetime

DATA_FILE = "trainings.json"

class TrainingPlanner:
    def init(self, root):
        self.root = root
        self.root.title("Training Planner")

        # Поля ввода
        tk.Label(root, text="Дата (YYYY-MM-DD)").grid(row=0, column=0)
        self.date_entry = tk.Entry(root)
        self.date_entry.grid(row=0, column=1)

        tk.Label(root, text="Тип тренировки").grid(row=1, column=0)
        self.type_entry = tk.Entry(root)
        self.type_entry.grid(row=1, column=1)

        tk.Label(root, text="Длительность (мин)").grid(row=2, column=0)
        self.duration_entry = tk.Entry(root)
        self.duration_entry.grid(row=2, column=1)

        # Кнопка добавления
        tk.Button(root, text="Добавить тренировку", command=self.add_training).grid(row=3, columnspan=2)

        # Фильтры
        tk.Label(root, text="Фильтр по типу").grid(row=4, column=0)
        self.filter_type = tk.Entry(root)
        self.filter_type.grid(row=4, column=1)

        tk.Label(root, text="Фильтр по дате").grid(row=5, column=0)
        self.filter_date = tk.Entry(root)
        self.filter_date.grid(row=5, column=1)

        tk.Button(root, text="Применить фильтр", command=self.apply_filter).grid(row=6, columnspan=2)

        # Таблица
        self.tree = ttk.Treeview(root, columns=("date", "type", "duration"), show="headings")
        self.tree.heading("date", text="Дата")
        self.tree.heading("type", text="Тип")
        self.tree.heading("duration", text="Длительность")
        self.tree.grid(row=7, columnspan=2)

        self.trainings = []
        self.load_data()

    def validate(self, date, duration):
        try:
            datetime.strptime(date, "%Y-%m-%d")
        except:
            messagebox.showerror("Ошибка", "Неверный формат даты!")
            return False

        try:
            if int(duration) <= 0:
                raise ValueError
        except:
            messagebox.showerror("Ошибка", "Длительность должна быть положительным числом!")
            return False

        return True

    def add_training(self):
        date = self.date_entry.get()
        ttype = self.type_entry.get()
        duration = self.duration_entry.get()

        if not self.validate(date, duration):
            return

        training = {
            "date": date,
            "type": ttype,
            "duration": int(duration)
        }

        self.trainings.append(training)
        self.save_data()
        self.update_table(self.trainings)

    def update_table(self, data):
        for row in self.tree.get_children():
            self.tree.delete(row)

        for t in data:
            self.tree.insert("", tk.END, values=(t["date"], t["type"], t["duration"]))

    def apply_filter(self):
        f_type = self.filter_type.get().lower()
        f_date = self.filter_date.get()

        filtered = [
            t for t in self.trainings
            if (f_type in t["type"].lower() if f_type else True)
            and (t["date"] == f_date if f_date else True)
        ]

        self.update_table(filtered)

    def save_data(self):
        with open(DATA_FILE, "w") as f:
            json.dump(self.trainings, f, indent=4)

    def load_data(self):
        try:
            with open(DATA_FILE, "r") as f:
                self.trainings = json.load(f)
                self.update_table(self.trainings)
        except:
            self.trainings = []


if name == "main":
    root = tk.Tk()
    app = TrainingPlanner(root)
    root.mainloop()
