BEGIN;

INSERT INTO author (name) VALUES
    ('Ada Fictícia'),
    ('Linus Exemplo'),
    ('Grace Demonstração');

INSERT INTO book (isbn, title, genre, published_year) VALUES
    ('9780000000001', 'Modelagem sem mistério', 'databases', 2024),
    ('9780000000002', 'APIs que duram', 'software', 2025),
    ('9780000000003', 'Concorrência prática', 'systems', 2023);

INSERT INTO book_author (book_id, author_id, author_order) VALUES
    (1, 1, 1),
    (2, 1, 1),
    (2, 2, 2),
    (3, 3, 1);

INSERT INTO copy (book_id, acquired_at, status) VALUES
    (1, DATE '2026-01-10', 'loaned'),
    (1, DATE '2026-01-10', 'available'),
    (2, DATE '2026-02-15', 'available'),
    (3, DATE '2026-03-20', 'available');

INSERT INTO member (display_name, email, joined_at) VALUES
    ('Pessoa Um', 'pessoa1@example.test', TIMESTAMPTZ '2026-01-01 12:00:00Z'),
    ('Pessoa Dois', 'pessoa2@example.test', TIMESTAMPTZ '2026-02-01 12:00:00Z'),
    ('Pessoa Sem Empréstimo', 'pessoa3@example.test', TIMESTAMPTZ '2026-03-01 12:00:00Z');

INSERT INTO loan (copy_id, member_id, borrowed_at, due_at, returned_at) VALUES
    (1, 1, TIMESTAMPTZ '2026-08-01 12:00:00Z', TIMESTAMPTZ '2026-08-15 12:00:00Z', TIMESTAMPTZ '2026-08-12 12:00:00Z'),
    (1, 2, TIMESTAMPTZ '2026-09-01 12:00:00Z', TIMESTAMPTZ '2026-09-15 12:00:00Z', NULL),
    (3, 1, TIMESTAMPTZ '2026-07-01 12:00:00Z', TIMESTAMPTZ '2026-07-15 12:00:00Z', TIMESTAMPTZ '2026-07-14 12:00:00Z');

COMMIT;
