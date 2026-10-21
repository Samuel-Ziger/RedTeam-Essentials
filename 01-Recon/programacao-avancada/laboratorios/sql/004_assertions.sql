\set ON_ERROR_STOP on

-- Este arquivo transforma expectativas do laboratório em testes executáveis.
DO $$
BEGIN
    IF (SELECT count(*) FROM author) <> 3 THEN
        RAISE EXCEPTION 'esperados 3 autores';
    END IF;
    IF (SELECT count(*) FROM book) <> 3 THEN
        RAISE EXCEPTION 'esperados 3 livros';
    END IF;
    IF (SELECT count(*) FROM loan WHERE returned_at IS NULL) <> 1 THEN
        RAISE EXCEPTION 'esperado exatamente 1 empréstimo aberto';
    END IF;
    IF EXISTS (
        SELECT copy_id
        FROM loan
        WHERE returned_at IS NULL
        GROUP BY copy_id
        HAVING count(*) > 1
    ) THEN
        RAISE EXCEPTION 'um exemplar possui mais de um empréstimo aberto';
    END IF;
END
$$;

-- A restrição de ISBN deve rejeitar entrada fora do domínio.
DO $$
BEGIN
    BEGIN
        INSERT INTO book (isbn, title, genre, published_year)
        VALUES ('invalid', 'Não deve persistir', 'test', 2026);
        RAISE EXCEPTION 'ISBN inválido foi aceito';
    EXCEPTION
        WHEN check_violation THEN NULL;
    END;
END
$$;

-- O índice parcial é também uma regra de concorrência: uma cópia não pode ter
-- dois empréstimos abertos ao mesmo tempo.
DO $$
BEGIN
    BEGIN
        INSERT INTO loan (copy_id, member_id, borrowed_at, due_at)
        VALUES (
            1,
            1,
            TIMESTAMPTZ '2026-10-01 12:00:00Z',
            TIMESTAMPTZ '2026-10-15 12:00:00Z'
        );
        RAISE EXCEPTION 'segundo empréstimo aberto foi aceito';
    EXCEPTION
        WHEN unique_violation THEN NULL;
    END;
END
$$;

-- Confere resultados sem depender da formatação de saída do psql.
DO $$
DECLARE
    members_without_loans bigint;
    books_without_loans bigint;
BEGIN
    SELECT count(*)
    INTO members_without_loans
    FROM member AS m
    WHERE NOT EXISTS (
        SELECT 1 FROM loan AS l WHERE l.member_id = m.id
    );

    SELECT count(*)
    INTO books_without_loans
    FROM book AS b
    WHERE NOT EXISTS (
        SELECT 1
        FROM copy AS c
        JOIN loan AS l ON l.copy_id = c.id
        WHERE c.book_id = b.id
    );

    IF members_without_loans <> 1 OR books_without_loans <> 1 THEN
        RAISE EXCEPTION
            'anti-joins divergiram: membros=%, livros=%',
            members_without_loans,
            books_without_loans;
    END IF;
END
$$;

SELECT 'ok' AS status,
       (SELECT count(*) FROM book) AS books,
       (SELECT count(*) FROM loan) AS loans;
