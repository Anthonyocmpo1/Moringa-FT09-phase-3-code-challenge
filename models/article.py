import sqlite3

class Article:
    def __init__(self, author, magazine, title):
        if not isinstance(title, str) or not (5 <= len(title) <= 50):
            raise ValueError("Title must be a string between 5 and 50 characters")

        self._title = title
        self._author_id = author.id
        self._magazine_id = magazine.id

        connection = sqlite3.connect('database.db')
        cursor = connection.cursor()
        cursor.execute("""
            INSERT INTO articles (title, author_id, magazine_id) 
            VALUES (?, ?, ?)
        """, (self._title, self._author_id, self._magazine_id))
        connection.commit()
        connection.close()

    @property
    def title(self):
        return self._title

    def author(self):
        connection = sqlite3.connect('database.db')
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM authors WHERE id = ?", (self._author_id,))
        author = cursor.fetchone()
        connection.close()
        return author

    def magazine(self):
        connection = sqlite3.connect('database.db')
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM magazines WHERE id = ?", (self._magazine_id,))
        magazine = cursor.fetchone()
        connection.close()
        return magazine
