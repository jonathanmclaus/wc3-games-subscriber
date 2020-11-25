CREATE TABLE subscriptions(
    -- ID
    unique_id    TEXT PRIMARY KEY,
    -- Key
    channel_id   INT,
    name         TEXT,
    -- Values
    creator_id   INT NOT NULL,
    file_pattern TEXT,
    name_pattern TEXT,
    realms       TEXT,   -- Comma separated list.
    PRIMARY KEY(channel_id, name)
)

CREATE TABLE games(
    -- ID
    unique_id       INT PRIMARY KEY
    -- Key
    name     TEXT,
    sever    TEXT,
    created  INT
    map      TEXT
    host

CREATE TABLE message(
    -- Key
    channel_id   INT,   -- Discord ID.
    user_id      INT,   -- Discord ID.
    name         TEXT,
    -- Values
    file_pattern TEXT,
    name_pattern TEXT,
    realm        TEXT   -- Comma separated list.
    PRIMARY KEY(channel_id, user_id, name)
)
