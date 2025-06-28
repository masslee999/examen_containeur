import logging
from pathlib import Path
from telegram import (ReplyKeyboardMarkup, ReplyKeyboardRemove, Update,
                      InlineKeyboardButton, InlineKeyboardMarkup)
from telegram.ext import (Application, CallbackQueryHandler, CommandHandler,
                          ContextTypes, ConversationHandler, MessageHandler, filters)
from dotenv import load_dotenv
import os
import mysql.connector

BASE_DIR = Path(__file__).resolve().parent.parent

# Chargement des variables d'environnement
load_dotenv(dotenv_path=BASE_DIR / '.env')

# Chargement des variables d'environnement
load_dotenv()

# Configuration du logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

# Définition des étapes de la conversation
NOMS, PRENOMS, EMAIL, PASSWORD, CONFIRMATION = range(5)


# Configuration de la connexion MySQL
def get_db_connection():
    return mysql.connector.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME")
    )


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Démarre la conversation et demande le nom de l'étudiant."""
    await update.message.reply_text(
        '<b>Bienvenue dans le bot d\'inscription des étudiants développeurs!\n'
        'Nous allons collecter vos informations.\n'
        'Quel est votre nom de famille?</b>',
        parse_mode='HTML',
        reply_markup=ReplyKeyboardRemove()
    )
    return NOMS


async def get_noms(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Stocke le nom de famille et demande le prénom."""
    context.user_data['noms'] = update.message.text
    await update.message.reply_text(
        '<b>Merci! Quel est votre prénom?</b>',
        parse_mode='HTML'
    )
    return PRENOMS


async def get_prenoms(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Stocke le prénom et demande l'email."""
    context.user_data['prenoms'] = update.message.text
    await update.message.reply_text(
        '<b>Parfait! Quel est votre email?</b>',
        parse_mode='HTML'
    )
    return EMAIL


async def get_email(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Stocke l'email et demande le mot de passe."""
    email = update.message.text
    if not '@' in email or '.' not in email.split('@')[1]:
        await update.message.reply_text(
            '<b>Email invalide. Veuillez entrer un email valide:</b>',
            parse_mode='HTML'
        )
        return EMAIL

    context.user_data['email'] = email
    await update.message.reply_text(
        '<b>Créez maintenant un mot de passe sécurisé:</b>',
        parse_mode='HTML'
    )
    return PASSWORD


async def get_password(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Stocke le mot de passe et demande confirmation."""
    context.user_data['password'] = update.message.text
    await update.message.reply_text(
        '<b>Confirmez votre mot de passe:</b>',
        parse_mode='HTML'
    )
    return CONFIRMATION


async def confirm_data(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Vérifie la confirmation et enregistre en base de données."""
    if update.message.text != context.user_data['password']:
        await update.message.reply_text(
            '<b>Les mots de passe ne correspondent pas. Veuillez réessayer:</b>',
            parse_mode='HTML'
        )
        return PASSWORD

    # Enregistrement dans la base de données
    conn = None
    cursor = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        query = """
        INSERT INTO DevStudents (fname, sname, email, mot_de_passe)
        VALUES (%s, %s, %s, %s)
        """
        values = (
            context.user_data['noms'],
            context.user_data['prenoms'],
            context.user_data['email'],
            context.user_data['password']  # Note: En production, il faudrait hasher le mot de passe
        )

        cursor.execute(query, values)
        conn.commit()

        await update.message.reply_text(
            '<b>Inscription réussie! Vos données ont été enregistrées.</b>',
            parse_mode='HTML'
        )

    except mysql.connector.Error as err:
        logger.error(f"Erreur MySQL: {err}")
        await update.message.reply_text(
            '<b>Une erreur est survenue lors de l\'enregistrement. Veuillez réessayer plus tard.</b>',
            parse_mode='HTML'
        )
    finally:
        if cursor is not None:
            cursor.close()
        if conn is not None and conn.is_connected():
            conn.close()

    return ConversationHandler.END


async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Annule et termine la conversation."""
    await update.message.reply_text(
        'Inscription annulée. À bientôt!',
        reply_markup=ReplyKeyboardRemove()
    )
    return ConversationHandler.END


def main() -> None:
    """Lance le bot."""
    application = Application.builder().token(os.environ["TOKEN"]).build()

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            NOMS: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_noms)],
            PRENOMS: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_prenoms)],
            EMAIL: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_email)],
            PASSWORD: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_password)],
            CONFIRMATION: [MessageHandler(filters.TEXT & ~filters.COMMAND, confirm_data)]
        },
        fallbacks=[CommandHandler('cancel', cancel)],
    )

    application.add_handler(conv_handler)
    application.run_polling()


if __name__ == '__main__':
    main()