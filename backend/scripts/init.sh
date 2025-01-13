#!/bin/bash

# change directory to backend
cd ..

current_dir=$(basename "$PWD")
echo $current_dir
if [ "$current_dir" = "backend" ]; then
    echo "change directory to backend"
else
    echo "directory not in backend"
    exit 0
fi

# check for os
os=$(uname)

if [ "$os" = "Darwin" ] || [ "$os" = "Linux" ]; then
    export FLASK_APP=src/app
    echo "FLASK_APP set to src/app.py (Unix-like system)"
else
    set FLASK_APP=src/app.py
    echo "FLASK_APP set to src/app.py (Windows system)"
fi

# database initialize
DB_NAME="database.db"
if [ -e "$DB_NAME" ]; then
    echo "databas.db already exists."
else
    echo "databas.db does not exist."
    flask init-db
fi

# genres initialize

sqlite3 "$DB_NAME" <<EOF
DROP TABLE IF EXISTS genre;
EOF

sqlite3 "$DB_NAME" <<EOF
CREATE TABLE genre (
    genre_id INTEGER PRIMARY KEY AUTOINCREMENT,
    genre_name TEXT, -- not null
    create_time DATETIME DEFAULT CURRENT_TIMESTAMP
);
EOF

sqlite3 "$DB_NAME" <<EOF
INSERT INTO genre (genre_name) VALUES 
('哲學類'), ('宗教類'),
('自然科學'), ('應用科學'), ('社會科學'),
('中國史地'), ('世界史地'),
('語文類'), ('藝術類');
EOF

echo "Initialize genre table."

flask run

