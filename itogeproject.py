import tkinter as tk
from tkinter import ttk, messagebox
import json
import os

class BookTracker:
    def __init__(self, root):
        self.root = root
        self.root.title("Book Tracker")
        
        # Поля ввода
        tk.Label(root, text="Название книги:").grid(row=0, column=0, padx=5, pady=5)
        self.title_entry = tk.Entry(root, width=30)
        self.title_entry.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(root, text="Автор:").grid(row=1, column=0, padx=5, pady=5)
        self.author_entry = tk.Entry(root, width=30)
        self.author_entry.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(root, text="Жанр:").grid(row=2, column=0, padx=5, pady=5)
        self.genre_entry = tk.Entry(root, width=30)
        self.genre_entry.grid(row=2, column=1, padx=5, pady=5)

        tk.Label(root, text="Количество страниц:").grid(row=3, column=0, padx=5, pady=5)
        self.pages_entry = tk.Entry(root, width=30)
        self.pages_entry.grid(row=3, column=1, padx=5, pady=5)

        # Кнопка добавления
        self.add_button = tk.Button(root, text="Добавить книгу", command=self.add_book)
        self.add_button.grid(row=4, column=0, columnspan=2, pady=10)

        # Таблица для отображения книг
        self.tree = ttk.Treeview(root, columns=("Title", "Author", "Genre", "Pages"), show="headings")
        self.tree.heading("Title", text="Название")
        self.tree.heading("Author", text="Автор")
        self.tree.heading("Genre", text="Жанр")
        self.tree.heading("Pages", text="Страниц")
        self.tree.grid(row=5, column=0, columnspan=2, padx=5, pady=5)
    def add_book(self):
        title = self.title_entry.get().strip()
        author = self.author_entry.get().strip()
        genre = self.genre_entry.get().strip()
        pages_text = self.pages_entry.get().strip()

        # Проверка на пустые поля
        if not all([title, author, genre, pages_text]):
            messagebox.showerror("Ошибка", "Все поля должны быть заполнены!")
            return

        # Проверка, что количество страниц — число
        try:
            pages = int(pages_text)
            if pages <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Ошибка", "Количество страниц должно быть положительным числом!")
            return

        # Добавляем в таблицу
        self.tree.insert("", "end", values=(title, author, genre, pages))

        # Очищаем поля ввода
        self.clear_entries()

    def clear_entries(self):
        self.title_entry.delete(0, tk.END)
        self.author_entry.delete(0, tk.END)
        self.genre_entry.delete(0, tk.END)
        self.pages_entry.delete(0, tk.END)
        # Элементы фильтрации
        tk.Label(root, text="Фильтр по жанру:").grid(row=6, column=0, padx=5, pady=5)
        self.filter_genre = tk.Entry(root, width=30)
        self.filter_genre.grid(row=6, column=1, padx=5, pady=5)

        tk.Label(root, text="Минимум страниц:").grid(row=7, column=0, padx=5, pady=5)
        self.min_pages = tk.Entry(root, width=30)
        self.min_pages.grid(row=7, column=1, padx=5, pady=5)

        self.filter_button = tk.Button(root, text="Применить фильтр", command=self.apply_filter)
        self.filter_button.grid(row=8, column=0, columnspan=2, pady=10)

    def apply_filter(self):
        genre_filter = self.filter_genre.get().lower()
        min_pages_filter = self.min_pages.get()

        try:
            min_pages = int(min_pages_filter) if min_pages_filter else 0
        except ValueError:
            messagebox.showerror("Ошибка", "Минимальное количество страниц должно быть числом!")
            return

        # Получаем все элементы таблицы
        items = self.tree.get_children()
        for item in items:
            values = self.tree.item(item, "values")
            genre_match = genre_filter in values[2].lower() if genre_filter else True
            pages_match = int(values[3]) >= min_pages

            if genre_match and pages_match:
                self.tree.item(item, tags=('visible',))
            else:
                self.tree.item(item, tags=('hidden',))

        self.tree.tag_configure('visible', foreground='black')
        self.tree.tag_configure('hidden', foreground='gray')

    def save_to_json(self):
        books = []
        for item in self.tree.get_children():
            books.append(self.tree.item(item, "values"))

        with open("books.json", "w", encoding="utf-8") as f:
            json.dump(books, f, ensure_ascii=False, indent=4)
        messagebox.showinfo("Успех", "Данные сохранены в books.json")

    def load_from_json(self):
        if os.path.exists("books.json"):
            with open("books.json", "r", encoding="utf-8") as f:
                books = json.load(f)
            for book in books:
                self.tree.insert("", "end", values=book)
            messagebox.showinfo("Успех", "Данные загружены из books.json")
        else:
            messagebox.showwarning("Предупреждение", "Файл books.json не найден")
        self.save_button = tk.Button(root, text="Сохранить в JSON", command=self.save_to_json)
        self.save_button.grid(row=9, column=0, pady=10)

        self.load_button = tk.Button(root, text="Загрузить из JSON", command=self.load_from_json)
        self.load_button.grid(row=9, column=1, pady=10)
if __name__ == "__main__":
    root = tk.Tk()
    app = BookTracker(root)
    root.mainloop()
