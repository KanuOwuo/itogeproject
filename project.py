import tkinter as tk from tkinter
import ttk, messagebox
import json
import os

class BookTracker:
    def __init__(self, root):
        self.root = root
        self.root.title("Book Tracker")
        self.books = []
        self.load_data()
        self.create_widgets()

    def create_widgets(self):
        # Поля ввода
        tk.Label(self.root, text="Название книги:").grid(row=0, column=0, sticky="w", padx=5, pady=5)
        self.title_entry = tk.Entry(self.root, width=40)
        self.title_entry.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(self.root, text="Автор:").grid(row=1, column=0, sticky="w", padx=5, pady=5)
        self.author_entry = tk.Entry(self.root, width=40)
        self.author_entry.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(self.root, text="Жанр:").grid(row=2, column=0, sticky="w", padx=5, pady=5)
        self.genre_entry = tk.Entry(self.root, width=40)
        self.genre_entry.grid(row=2, column=1, padx=5, pady=5)

        tk.Label(self.root, text="Количество страниц:").grid(row=3, column=0, sticky="w", padx=5, pady=5)
        self.pages_entry = tk.Entry(self.root, width=40)
        self.pages_entry.grid(row=3, column=1, padx=5, pady=5)

        # Кнопка добавления
        self.add_button = tk.Button(self.root, text="Добавить книгу", command=self.add_book)
        self.add_button.grid(row=4, column=0, columnspan=2, pady=10)

        # Таблица
        self.tree = ttk.Treeview(self.root, columns=("Title", "Author", "Genre", "Pages"), show="headings")
        self.tree.heading("Title", text="Название")
        self.tree.heading("Author", text="Автор")
        self.tree.heading("Genre", text="Жанр")
        self.tree.heading("Pages", text="Страниц")
        self.tree.grid(row=5, column=0, columnspan=2, padx=5, pady=5, sticky="nsew")

        # Фильтры
        tk.Label(self.root, text="Фильтр по жанру:").grid(row=6, column=0, sticky="w", padx=5, pady=5)
        self.genre_filter = tk.Entry(self.root, width=20)
        self.genre_filter.grid(row=6, column=1, sticky="w", padx=5, pady=5)

        tk.Label(self.root, text="Фильтр страниц (>):").grid(row=7, column=0, sticky="w", padx=5, pady=5)
        self.pages_filter = tk.Entry(self.root, width=20)
        self.pages_filter.grid(row=7, column=1, sticky="w", padx=5, pady=5)

        self.filter_button = tk.Button(self.root, text="Применить фильтры", command=self.apply_filters)
        self.filter_button.grid(row=8, column=0, columnspan=2, pady=5)

        self.clear_filter_button = tk.Button(self.root, text="Сбросить фильтры", command=self.load_data)
        self.clear_filter_button.grid(row=9, column=0, columnspan=2, pady=5)

        # Кнопки сохранения/загрузки
        self.save_button = tk.Button(self.root, text="Сохранить в JSON", command=self.save_data)
        self.save_button.grid(row=10, column=0, pady=5)

        self.load_button = tk.Button(self.root, text="Загрузить из JSON", command=self.load_data)
        self.load_button.grid(row=10, column=1, pady=5)
def add_book(self):
    title = self.title_entry.get().strip()
    author = self.author_entry.get().strip()
    genre = self.genre_entry.get().strip()
    pages_text = self.pages_entry.get().strip()

    # Проверка валидации
    if not title or not author or not genre:
        messagebox.showerror("Ошибка", "Все поля, кроме количества страниц, обязательны!")
        return

    try:
        pages = int(pages_text) if pages_text else 0
        if pages < 0:
            messagebox.showerror("Ошибка", "Количество страниц не может быть отрицательным!")
            return
    except ValueError:
        messagebox.showerror("Ошибка", "Количество страниц должно быть числом!")
        return

    # Добавляем книгу
    book = {"title": title, "author": author, "genre": genre, "pages": pages}
    self.books.append(book)

    # Очищаем поля
    self.title_entry.delete(0, tk.END)
    self.author_entry.delete(0, tk.END)
    self.genre_entry.delete(0, tk.END)
    self.pages_entry.delete(0, tk.END)

    self.update_table()

def apply_filters(self):
    filtered_books = self.books

    genre_filter = self.genre_filter.get().strip().lower()
    if genre_filter:
        filtered_books = [b for b in filtered_books if genre_filter in b["genre"].lower()]

    pages_filter_text = self.pages_filter.get().strip()
    if pages_filter_text:
        try:
            min_pages = int(pages_filter_text)
            filtered_books = [b for b in filtered_books if b["pages"] >= min_pages
        except ValueError:
            messagebox.showerror("Ошибка", "Некорректное значение для фильтра страниц!")
            return

    self.update_table(filtered_books)

def update_table(self, books=None):
    for item in self.tree.get_children():
        self.tree.delete(item)

    target_books = books if books is not None else self.books
    for book in target_books:
        self.tree.insert("", "end", values=(book["title"], book["author"], book["genre"], book["pages"]))
 def save_data(self):
    with open("books.json", "w", encoding="utf-8") as f:
        json.dump(self.books, f, ensure_ascii=False, indent=4)
    messagebox.showinfo("Успех", "Данные сохранены в books.json")

def load_data(self):
    if os.path.exists("books.json"):
        with open("books.json", "r", encoding="utf-8") as f:
            self.books = json.load(f)
    else:
        self.books = []
    self.update_table()
if __name__ == "__main__":
    root = tk.Tk()   
