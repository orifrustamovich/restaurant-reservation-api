# 1-qator: Qaysi "asos" image ishlatamiz?
# python:3.11-slim = Python 3.11 o'rnatilgan, yengil Linux
FROM python:3.11-slim

# Muhit o'zgaruvchilari
# PYTHONDONTWRITEBYTECODE=1 → .pyc fayllar yaratilmaydi (kerak emas)
# PYTHONUNBUFFERED=1 → print() va log'lar darhol ko'rinadi
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Container ichida ishchi papka
# /app papkasi bo'lmasa, Docker o'zi yaratadi
WORKDIR /app

# AVVAL requirements.txt ko'chiramiz — nima uchun?
# Docker har bir qatorni "layer" sifatida saqlaydi.
# Agar faqat .py fayllar o'zgarse, pip install qayta ishlamaydi.
# Bu build vaqtini 2-3 daqiqadan 10 sekundga tushiradi.
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Keyin barcha kodni ko'chiramiz
COPY . .

# entrypoint.sh ni bajariladigan qilamiz
COPY entrypoint.sh .
RUN chmod +x entrypoint.sh

# Container 8000-portni "tinglaydi" deb belgilaymiz
# Bu faqat hujjat — haqiqiy port ochish docker-compose'da
EXPOSE 8000

# Container ishga tushganda shu script bajariladi
ENTRYPOINT ["./entrypoint.sh"]