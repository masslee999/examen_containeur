FROM python:3.10

WORKDIR /app

# Copier les fichiers nécessaires
COPY requirements.txt .
COPY telegram_bot.py .

# Installer les dépendances
RUN pip install --upgrade pip && pip install -r requirements.txt

# Lancer le bot
CMD ["python", "telegram_bot.py"]
