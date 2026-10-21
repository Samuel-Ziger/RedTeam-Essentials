BEGIN;

DROP TABLE IF EXISTS loan;
DROP TABLE IF EXISTS copy;
DROP TABLE IF EXISTS book_author;
DROP TABLE IF EXISTS book;
DROP TABLE IF EXISTS author;
DROP TABLE IF EXISTS member;

CREATE TABLE author (
    id bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    name varchar(120) NOT NULL,
    CONSTRAINT author_name_unique UNIQUE (name)
);

CREATE TABLE book (
    id bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    isbn varchar(13) NOT NULL UNIQUE CHECK (isbn ~ '^[0-9]{13}$'),
    title varchar(200) NOT NULL CHECK (length(trim(title)) > 0),
    genre varchar(40) NOT NULL,
    published_year integer CHECK (published_year BETWEEN 1450 AND 2100)
);

CREATE TABLE book_author (
    book_id bigint NOT NULL REFERENCES book(id) ON DELETE CASCADE,
    author_id bigint NOT NULL REFERENCES author(id) ON DELETE RESTRICT,
    author_order smallint NOT NULL CHECK (author_order > 0),
    PRIMARY KEY (book_id, author_id),
    UNIQUE (book_id, author_order)
);

CREATE TABLE copy (
    id bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    book_id bigint NOT NULL REFERENCES book(id) ON DELETE RESTRICT,
    acquired_at date NOT NULL,
    status varchar(12) NOT NULL DEFAULT 'available'
        CHECK (status IN ('available', 'loaned', 'retired'))
);

CREATE TABLE member (
    id bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    display_name varchar(120) NOT NULL,
    email varchar(254) NOT NULL UNIQUE,
    joined_at timestamptz NOT NULL DEFAULT now()
);

CREATE TABLE loan (
    id bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    copy_id bigint NOT NULL REFERENCES copy(id) ON DELETE RESTRICT,
    member_id bigint NOT NULL REFERENCES member(id) ON DELETE RESTRICT,
    borrowed_at timestamptz NOT NULL,
    due_at timestamptz NOT NULL,
    returned_at timestamptz,
    CHECK (due_at > borrowed_at),
    CHECK (returned_at IS NULL OR returned_at >= borrowed_at)
);

CREATE UNIQUE INDEX one_open_loan_per_copy
ON loan (copy_id)
WHERE returned_at IS NULL;

CREATE INDEX loan_member_borrowed_idx
ON loan (member_id, borrowed_at DESC);

COMMIT;
