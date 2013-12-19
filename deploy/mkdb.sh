#!/bin/bash

create_table () {
    echo "
CREATE TABLE link_store (
    id          INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    owner       TEXT NOT NULL,
    url         TEXT NOT NULL UNIQUE,
    active      BOOLEAN NOT NULL DEFAULT FALSE,
    file        TEXT,
    -- files       TEXT[1] NOT NULL DEFAULT ARRAY[]::TEXT[1],
    -- expire      TIMESTAMP WITHOUT TIMEZONE NOT NULL DEFAULT TOMORROW()
    get_limit   INTEGER NOT NULL DEFAULT -1,
    get_count   INTEGER NOT NULL DEFAULT 0
);
"
}

if [[ -n "$1" ]]; then
    dbname="$1.db"
    create_table | sqlite3 $dbname
    echo "Created $dbname."
else
    echo "-- usage: $0 [dbname]"
    echo
    echo "-- this script will create a linkstore using sqlite3 as follows:"
    create_table
fi
