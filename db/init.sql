CREATE TABLE IF NOT EXISTS books (
    id SERIAL PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    author VARCHAR(255) NOT NULL,
    genre VARCHAR(100),
    year INTEGER,
    is_available BOOLEAN DEFAULT TRUE
);

CREATE TABLE IF NOT EXISTS readers (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL
);

CREATE TABLE IF NOT EXISTS loans (
    id SERIAL PRIMARY KEY,
    book_id INTEGER REFERENCES books(id) ON DELETE CASCADE,
    reader_id INTEGER REFERENCES readers(id) ON DELETE CASCADE,
    loan_date DATE NOT NULL DEFAULT CURRENT_DATE,
    return_date DATE
);

INSERT INTO books (title, author, genre, year) VALUES
    ('Война и мир', 'Лев Толстой', 'Роман', 1869),
    ('Преступление и наказание', 'Фёдор Достоевский', 'Роман', 1866),
    ('Мастер и Маргарита', 'Михаил Булгаков', 'Роман', 1967),
    ('Анна Каренина', 'Лев Толстой', 'Роман', 1877),
    ('Идиот', 'Фёдор Достоевский', 'Роман', 1869)
ON CONFLICT (id) DO NOTHING;

INSERT INTO readers (name, email) VALUES
    ('Иван Петров', 'ivan@email.com'),
    ('Мария Сидорова', 'maria@email.com'),
    ('Петр Иванов', 'petr@email.com')
ON CONFLICT (email) DO NOTHING;

INSERT INTO loans (book_id, reader_id, loan_date) VALUES
   (1, 1, CURRENT_DATE - INTERVAL '7 days'),
   (2, 2, CURRENT_DATE - INTERVAL '3 days');