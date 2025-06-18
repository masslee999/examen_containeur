from telegram import (
    ReplyKeyboardMarkup, 
    InlineKeyboardButton, 
    InlineKeyboardMarkup, 
    Update
)
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    ConversationHandler,
    ContextTypes,
    filters
)

# États de la conversation
CAR_TYPE, CAR_COLOR, CAR_YEAR, CAR_MILEAGE, CAR_PHOTO, CAR_CONFIRMATION = range(6)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text(
        "🚗 Bienvenue sur AutoBot! Créons ensemble votre annonce.\n"
        "Utilisez /cancel pour annuler."
    )
    return await ask_car_type(update, context)

async def ask_car_type(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    buttons = [['Sedan', 'SUV'], ['Hatchback', 'Convertible'], ['Break', 'Autre']]
    reply_markup = ReplyKeyboardMarkup(buttons, one_time_keyboard=True)
    await update.message.reply_text('Sélectionnez le type:', reply_markup=reply_markup)
    return CAR_TYPE

async def receive_car_type(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data['car_type'] = update.message.text
    return await ask_car_color(update, context)

async def ask_car_color(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    buttons = [['Noir', 'Blanc', 'Gris'], ['Rouge', 'Bleu', 'Vert'], ['Autre']]
    reply_markup = ReplyKeyboardMarkup(buttons, one_time_keyboard=True)
    await update.message.reply_text('🎨 Quelle est la couleur principale?', reply_markup=reply_markup)
    return CAR_COLOR

async def receive_car_color(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data['car_color'] = update.message.text
    return await ask_car_year(update, context)

async def skip_color(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data['car_color'] = "Non spécifiée"
    await update.message.reply_text("Pas de couleur spécifiée.")
    return await ask_car_year(update, context)

async def ask_car_year(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    buttons = [['2020-2023', '2017-2020'], ['2010-2017', 'Avant 2010']]
    reply_markup = ReplyKeyboardMarkup(buttons, one_time_keyboard=True)
    await update.message.reply_text('📅 Quelle est l\'année de fabrication?', reply_markup=reply_markup)
    return CAR_YEAR

async def receive_car_year(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data['car_year'] = update.message.text
    return await ask_car_mileage(update, context)

async def ask_car_mileage(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text('🔢 Quel est le kilométrage actuel? (en km)\nExemple: 75000')
    return CAR_MILEAGE

async def receive_car_mileage(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    try:
        mileage = int(update.message.text)
        context.user_data['car_mileage'] = f"{mileage:,} km".replace(",", " ")
        return await ask_car_photo(update, context)
    except ValueError:
        await update.message.reply_text("❌ Veuillez entrer un nombre valide.")
        return CAR_MILEAGE

async def ask_car_photo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text('📸 Envoyez une photo de votre voiture (optionnel)\nou /skip pour passer.')
    return CAR_PHOTO

async def receive_car_photo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    photo_file = await update.message.photo[-1].get_file()
    context.user_data['car_photo'] = photo_file.file_id
    return await summary(update, context)

async def skip_photo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data['car_photo'] = None
    return await summary(update, context)

async def summary(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user_data = context.user_data
    summary_text = (
        "📋 Récapitulatif:\n\n"
        f"• Type: {user_data.get('car_type', 'Non spécifié')}\n"
        f"• Couleur: {user_data.get('car_color', 'Non spécifiée')}\n"
        f"• Année: {user_data.get('car_year', 'Non spécifiée')}\n"
        f"• Kilométrage: {user_data.get('car_mileage', 'Non spécifié')}\n"
    )
    
    keyboard = [
        [InlineKeyboardButton("✅ Confirmer", callback_data='confirm_yes')],
        [InlineKeyboardButton("🔄 Recommencer", callback_data='confirm_no')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    if 'car_photo' in user_data and user_data['car_photo']:
        await update.message.reply_photo(
            photo=user_data['car_photo'],
            caption=summary_text,
            reply_markup=reply_markup
        )
    else:
        await update.message.reply_text(summary_text, reply_markup=reply_markup)
    
    return CAR_CONFIRMATION

async def confirm(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    query = update.callback_query
    await query.answer()
    
    if query.data == 'confirm_yes':
        await query.edit_message_text("✅ Annonce publiée!")
        return ConversationHandler.END
    else:
        await query.edit_message_text("🔄 Recommençons...")
        return await start(update, context)

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text('❌ Opération annulée.')
    return ConversationHandler.END

def main() -> None:
    application = Application.builder().token("7298952862:AAEgrR993virwTUc4xjZF-AvSSbHNkCatCY").build()

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            CAR_TYPE: [MessageHandler(filters.TEXT & ~filters.COMMAND, receive_car_type)],
            CAR_COLOR: [
                CommandHandler('skip', skip_color),
                MessageHandler(filters.TEXT & ~filters.COMMAND, receive_car_color)
            ],
            CAR_YEAR: [MessageHandler(filters.TEXT & ~filters.COMMAND, receive_car_year)],
            CAR_MILEAGE: [MessageHandler(filters.TEXT & ~filters.COMMAND, receive_car_mileage)],
            CAR_PHOTO: [
                MessageHandler(filters.PHOTO, receive_car_photo),
                CommandHandler('skip', skip_photo)
            ],
            CAR_CONFIRMATION: [CallbackQueryHandler(confirm, pattern='^confirm_')]
        },
        fallbacks=[CommandHandler('cancel', cancel)],
        allow_reentry=True
    )

    application.add_handler(conv_handler)
    application.run_polling()

if __name__ == '__main__':
    main()
