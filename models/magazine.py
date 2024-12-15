import sqlite3

class Magazine:
    def __init__(self, id, name, category):
        if not isinstance(name, str) or not (2 <= len(name) <= 16):
            raise ValueError("Name must be a string between 2 and 16 characters")
        if not isinstance(category, str) or len(category) == 0:
            raise ValueError("Category must be a non-empty string")

        self._id = id
        self._name = name
        self._category = category

        connection = sqlite3.connect('database.db')
        cursor = connection.cursor()
        cursor.execute("INSERT INTO magazines (id, name, category) VALUES (?, ?, ?)", 
                       (self._id, self._name, self._category))
        connection.commit()
        connection.close()

    @property
    def id(self):
        return self._id

    @property
    def name(self):
        return self._name

    @property
    def category(self):
        return self._category

    def articles(self):
        connection = sqlite3.connect('database.db')
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM articles WHERE magazine_id = ?", (self.id,))
        articles = cursor.fetchall()
        connection.close()
        return articles

    def contributors(self):
        connection = sqlite3.connect('database.db')
        cursor = connection.cursor()
        cursor.execute("""
            SELECT DISTINCT a.id, a.name
            FROM authors a
            JOIN articles ar ON ar.author_id = a.id
            WHERE ar.magazine_id = ?
        """, (self.id,))
        contributors = cursor.fetchall()
        connection.close()
        return contributors

    def article_titles(self):
        connection = sqlite3.connect('database.db')
        cursor = connection.cursor()
        cursor.execute("SELECT title FROM articles WHERE magazine_id = ?", (self.id,))
        titles = [row[0] for row in cursor.fetchall()]
        connection.close()
        return titles if titles else None

    def contributing_authors(self):
        connection = sqlite3.connect('database.db')
        cursor = connection.cursor()
        cursor.execute("""
            SELECT a.id, a.name, COUNT(*) as article_count
            FROM authors a
            JOIN articles ar ON ar.author_id = a.id
            WHERE ar.magazine_id = ?
            GROUP BY a.id
            HAVING article_count > 2
        """, (self.id,))
        authors = cursor.fetchall()
        connection.close()
        return authors if authors else None
