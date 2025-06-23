from telegram import (
    Update,
    ReplyKeyboardMarkup,
    InlineKeyboardButton,
    InlineKeyboardMarkup
)
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ConversationHandler,
    CallbackQueryHandler,
    ContextTypes,
    filters
)
import mysql.connector
import logging
from datetime import datetime

# Configuration
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# États de la conversation
USERNAME, LASTNAME, FIRSTNAME, PASSWORD, CONFIRM = range(5)

# Connexion MySQL
def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="telegram_bot_db"
    )

# Commandes
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text(
        "👋 Bienvenue dans le bot d'enregistrement !\n"
        "Commencez par entrer votre nom d'utilisateur :\n"
        "(ou /cancel pour annuler)"
    )
    return USERNAME

async def handle_username(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data['username'] = update.message.text
    await update.message.reply_text("Entrez votre nom de famille :")
    return LASTNAME

async def handle_lastname(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data['lastname'] = update.message.text
    await update.message.reply_text(
        "Entrez votre prénom (ou /skip pour passer) :",
        reply_markup=ReplyKeyboardMarkup([['/skip']], one_time_keyboard=True)
    )
    return FIRSTNAME

async def handle_firstname(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data['firstname'] = update.message.text
    await update.message.reply_text("Créez un mot de passe :")
    return PASSWORD

async def skip_firstname(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data['firstname'] = "Non spécifié"
    await update.message.reply_text("Aucun prénom enregistré.")
    await update.message.reply_text("Créez un mot de passe :")
    return PASSWORD

async def handle_password(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data['password'] = update.message.text
    return await show_summary(update, context)

async def show_summary(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user = context.user_data
    summary = (
        "📋 Récapitulatif :\n\n"
        f"🔹 Nom d'utilisateur: {user['username']}\n"
        f"🔹 Nom: {user['lastname']}\n"
        f"🔹 Prénom: {user.get('firstname', 'Non spécifié')}\n"
        f"🔹 Mot de passe: {'*' * len(user['password'])}"
    )

    keyboard = [
        [InlineKeyboardButton("✅ Confirmer", callback_data="confirm")],
        [InlineKeyboardButton("🔄 Recommencer", callback_data="restart")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(summary, reply_markup=reply_markup)
    return CONFIRM

async def save_to_database(user_data: dict) -> bool:
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute(
            "INSERT INTO users (username, lastname, firstname, password, created_at) "
            "VALUES (%s, %s, %s, %s, %s)",
            (
                user_data['username'],
                user_data['lastname'],
                user_data.get('firstname', ''),
                user_data['password'],
                datetime.now()
            )
        )
        conn.commit()
        return True
    except Exception as e:
        logging.error(f"Erreur MySQL: {e}")
        return False
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()

async def handle_confirmation(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    query = update.callback_query
    await query.answer()

    if query.data == "confirm":
        if await save_to_database(context.user_data):
            await query.edit_message_text("✅ Enregistrement réussi !")
        else:
            await query.edit_message_text("❌ Erreur lors de l'enregistrement.")
    else:
        await query.edit_message_text("Redémarrage...")
        return await start(update, context)
    
    return ConversationHandler.END

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text("❌ Opération annulée.")
    return ConversationHandler.END

def main() -> None:
    application = Application.builder().token("VOTRE_TOKEN").build()

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            USERNAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_username)],
            LASTNAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_lastname)],
            FIRSTNAME: [
                CommandHandler('skip', skip_firstname),
                MessageHandler(filters.TEXT & ~filters.COMMAND, handle_firstname)
            ],
            PASSWORD: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_password)],
            CONFIRM: [CallbackQueryHandler(handle_confirmation, pattern='^(confirm|restart)$')]
        },
        fallbacks=[CommandHandler('cancel', cancel)]
    )

    application.add_handler(conv_handler)
    application.run_polling()

if __name__ == '__main__':
    # Créer la table si elle n'existe pas
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INT AUTO_INCREMENT PRIMARY KEY,
            username VARCHAR(50) UNIQUE NOT NULL,
            lastname VARCHAR(50) NOT NULL,
            firstname VARCHAR(50),
            password VARCHAR(100) NOT NULL,
            created_at DATETIME NOT NULL
        )
    """)
    conn.close()
    
    main()
