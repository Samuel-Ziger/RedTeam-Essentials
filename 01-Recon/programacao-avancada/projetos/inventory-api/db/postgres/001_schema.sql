BEGIN;

CREATE TABLE IF NOT EXISTS product (
    id uuid PRIMARY KEY,
    sku varchar(32) NOT NULL,
    name varchar(120) NOT NULL,
    price_cents bigint NOT NULL CHECK (price_cents >= 0),
    stock integer NOT NULL DEFAULT 0 CHECK (stock >= 0),
    version integer NOT NULL DEFAULT 1 CHECK (version > 0),
    created_at timestamptz NOT NULL,
    updated_at timestamptz NOT NULL,
    CONSTRAINT product_sku_unique UNIQUE (sku),
    CHECK (length(trim(name)) BETWEEN 1 AND 120)
);

CREATE TABLE IF NOT EXISTS stock_movement (
    id uuid PRIMARY KEY,
    product_id uuid NOT NULL REFERENCES product(id) ON DELETE RESTRICT,
    delta integer NOT NULL CHECK (delta <> 0),
    reason varchar(120) NOT NULL CHECK (length(trim(reason)) > 0),
    resulting_stock integer NOT NULL CHECK (resulting_stock >= 0),
    resulting_version integer NOT NULL CHECK (resulting_version > 0),
    created_at timestamptz NOT NULL
);

CREATE TABLE IF NOT EXISTS idempotency_record (
    scope varchar(160) NOT NULL,
    key varchar(128) NOT NULL,
    request_hash char(64) NOT NULL,
    response_body jsonb,
    created_at timestamptz NOT NULL DEFAULT now(),
    PRIMARY KEY (scope, key)
);

CREATE TABLE IF NOT EXISTS outbox_event (
    id uuid PRIMARY KEY,
    aggregate_id uuid NOT NULL,
    event_type varchar(80) NOT NULL,
    payload jsonb NOT NULL,
    occurred_at timestamptz NOT NULL,
    published_at timestamptz
);

CREATE INDEX IF NOT EXISTS product_page_idx
ON product (created_at DESC, id DESC);

CREATE INDEX IF NOT EXISTS stock_movement_product_idx
ON stock_movement (product_id, created_at DESC, id DESC);

CREATE INDEX IF NOT EXISTS outbox_pending_idx
ON outbox_event (occurred_at, id)
WHERE published_at IS NULL;

COMMIT;
