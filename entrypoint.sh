#!/bin/sh

echo "PostgreSQL kutilmoqda..."
python << EOF
import socket
import time

while True:
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect(("db", 5432))
        s.close()
        break
    except:
        time.sleep(0.5)
EOF

echo "PostgreSQL tayyor!"

python manage.py migrate
python manage.py collectstatic --noinput
python manage.py runserver 0.0.0.0:8000