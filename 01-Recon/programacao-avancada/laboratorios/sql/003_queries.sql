\pset null '(null)'
\timing on

-- Join e agregação preservando livros sem empréstimo.
SELECT b.title,
       count(l.id) AS loans,
       count(l.id) FILTER (WHERE l.returned_at IS NULL) AS open_loans
FROM book AS b
LEFT JOIN copy AS c ON c.book_id = b.id
LEFT JOIN loan AS l ON l.copy_id = c.id
GROUP BY b.id, b.title
ORDER BY loans DESC, b.title;

-- Anti-join: membros que nunca fizeram empréstimo.
SELECT m.id, m.display_name
FROM member AS m
WHERE NOT EXISTS (
    SELECT 1 FROM loan AS l WHERE l.member_id = m.id
)
ORDER BY m.id;

-- Window function: ordem dos empréstimos de cada membro.
SELECT m.display_name,
       b.title,
       l.borrowed_at,
       row_number() OVER (
           PARTITION BY m.id
           ORDER BY l.borrowed_at, l.id
       ) AS member_loan_number
FROM loan AS l
JOIN member AS m ON m.id = l.member_id
JOIN copy AS c ON c.id = l.copy_id
JOIN book AS b ON b.id = c.book_id
ORDER BY m.id, member_loan_number;

-- Plano que deve considerar o índice parcial para empréstimo aberto por cópia.
EXPLAIN (ANALYZE, BUFFERS)
SELECT id, member_id, due_at
FROM loan
WHERE copy_id = 1 AND returned_at IS NULL;
