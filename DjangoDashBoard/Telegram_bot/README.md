
# 📦 Créer un Bot Telegram avec Python – Documentation Complète

Basée sur l’article de Moraneus : [Building Telegram Bot with Python](https://medium.com/@moraneus/building-telegram-bot-with-python-telegram-bot-a-comprehensive-guide-7e33f014dc79)

---

## 🌱 1. Préparer l’environnement

- **Créer un environnement virtuel**  
  ```bash
  python3 -m venv venv
  source venv/bin/activate
  ```

- **Installer les dépendances**  
  ```bash
  pip install -r requirements.txt
  ```

---

## 🤖 2. Créer votre bot Telegram

1. Ouvrir Telegram et rechercher **BotFather**
2. Envoyer la commande `/newbot`
3. Choisir un nom et un @username pour votre bot
![bot father chat](images/Capture_ecran_2025-06-13_181608.png)
4. **Copier le token** donné par BotFather 
5. Créer un fichier .env et inserer la paire clé-valeur:
```
TOKEN="your token here"
```

---

## 💻 3. Écrire le code du bot

Passons maintenant au codage du bot. Veuillez créer un nouveau fichier Python, par exemple : ```telegram_bot.py``` et ouvrez-le dans votre éditeur de texte préféré. Suivez ensuite ces étapes pour créer votre bot.

### Importer des bibliothèques :

Commencez par importer les modules nécessaires et configurer la journalisation pour faciliter le débogage :

```python
import logging
from telegram import (ReplyKeyboardMarkup, ReplyKeyboardRemove, Update, InlineKeyboardButton, InlineKeyboardMarkup)
from telegram.ext import (Application, CallbackQueryHandler, CommandHandler, ContextTypes, ConversationHandler, MessageHandler, filters)

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)
```

### Définir les états de conversation

Les états d’un bot Telegram, notamment lorsqu’un gestionnaire de conversations est utilisé, servent de cadre pour gérer le flux d’interaction entre le bot et l’utilisateur. Il s’agit essentiellement de marqueurs ou de points de contrôle qui définissent la partie de la conversation actuellement engagée par l’utilisateur et déterminent la prochaine action du bot en fonction de ses informations.

Voici un aperçu plus général du rôle et des fonctionnalités des états dans la gestion des conversations des bots. Leurs objectifs et fonctionnalités dans le bot Telegram sont les suivants :

---

#### 1. Gestion séquentielle des flux

Les états permettent au bot de gérer un flux de conversation séquentiel. En passant d’un état à un autre, le bot peut guider l’utilisateur à travers une série d’étapes, de questions ou d’options dans un ordre logique.

---

#### 2. Connaissance du contexte

Ces informations aident le robot à maintenir le contexte d’une conversation. En connaissant l’état actuel, le robot comprend les informations fournies par l’utilisateur et celles qui sont encore nécessaires, ce qui lui permet de réagir de manière appropriée.

---

#### 3. Traitement des saisies utilisateur

Selon l’état actuel, le bot peut traiter les saisies utilisateur différemment.  
Par exemple, une saisie `<get_noms>` sera interprétée comme une indication du nom de l'utilisateur à recueillir, tandis qu’une saisie `<get_email>` sera interprétée comme le mail de l'utilisateur.

---

#### 4. Implémentation de la logique conditionnelle

Les états permettent d’implémenter une logique conditionnelle dans la conversation.  
En fonction des réponses ou des choix de l’utilisateur, le bot peut décider d’ignorer certains états, de les répéter ou d’orienter l’utilisateur vers un autre chemin de conversation.

---

#### 5. Gestion des erreurs et répétition

Ils facilitent la gestion des erreurs et la répétition des questions si l’utilisateur fournit des réponses inexactes ou invalides.  
En suivant l’état actuel, le bot peut relancer l’utilisateur pour obtenir les informations correctes.

---

#### 6. Persistance de l’état

Dans les bots plus complexes, les états peuvent être stockés et conservés d’une session à l’autre, permettant aux utilisateurs de reprendre la conversation là où ils l’avaient laissée, même s’ils quittent temporairement le chat ou si le bot redémarre.


---

Énumérons les états pour que notre bot gère le flux :

```python
NOMS, PRENOMS, EMAIL, PASSWORD, CONFIRMATION = range(5)
```

## 🔁 4. Ajouter des fonctionnalités de conversation

Les gestionnaires de conversation des bots Telegram, notamment grâce à des bibliothèques comme `python-telegram-bot`, sont des outils puissants qui gèrent le flux des conversations en fonction des saisies utilisateur et d’états prédéfinis. Ils sont essentiels au développement de bots nécessitant une séquence d’interactions, comme la collecte d’informations, le guidage des utilisateurs dans les menus ou l’exécution de commandes dans un ordre précis.

Voici un aperçu détaillé du fonctionnement des gestionnaires de conversation et de leur rôle dans le développement de bots :

---

### Objectif et fonctionnalité

#### 1. Gestion des états conversationnels

Les gestionnaires de conversation suivent l’état actuel du dialogue avec chaque utilisateur. Ils déterminent la prochaine action du bot en fonction des informations saisies par l’utilisateur et de l’état actuel, permettant une progression fluide et logique des différentes étapes de l’interaction.

---

#### 2. Routage des entrées utilisateur

Ces entrées sont acheminées vers différentes fonctions de rappel en fonction de l’état actuel. Cela signifie qu’une même entrée peut produire des résultats différents selon la position de l’utilisateur dans la conversation.

---

#### 3. Gestion des commandes et du texte

Les gestionnaires de conversation peuvent faire la différence entre les commandes (comme `/start` ou `/help`) et les messages texte classiques, permettant aux développeurs de spécifier des réponses ou des actions distinctes pour chaque type d’entrée.

---

#### 4. Intégration avec les claviers et les boutons

Ils fonctionnent parfaitement avec les claviers personnalisés et les boutons intégrés, permettant aux développeurs de créer des interfaces interactives et conviviales au sein de la conversation.  
Les utilisateurs peuvent sélectionner des options ou naviguer parmi les fonctionnalités du bot grâce à ces éléments d’interface.

---

#### 5. Fonctions de reponse et d’expiration

Les gestionnaires de conversation prennent en charge les fonctions de reponse (reply), qui peuvent être déclenchées lorsque l’utilisateur entre une entrée inattendue ou lorsque la conversation doit être réinitialisée.  
Ils peuvent également gérer les expirations, mettant fin automatiquement à une conversation après une période d’inactivité.

La mise en œuvre d’un gestionnaire de conversation implique généralement la définition de **points d’entrée**, d’**états** et de **solutions de secours** :

- **Points d’entrée** :  
  Ce sont des déclencheurs qui lancent la conversation.  
  Généralement, la commande `/start` est utilisée comme point d’entrée, mais vous pouvez définir plusieurs points d’entrée pour différents flux de conversation.

- **États** :  
  Comme indiqué précédemment, les états représentent différents points de la conversation.  
  Chaque état est associé à une ou plusieurs fonctions de rappel qui définissent le comportement du bot à ce stade.  
  Les développeurs associent les états à ces fonctions de rappel, dictant ainsi le déroulement de la conversation.

- **Fonctions de secours** :  
  Les fonctions de secours sont définies pour gérer les situations imprévues ou pour permettre de quitter ou de réinitialiser la conversation.  
  Une fonction de secours courante est une commande `/cancel` permettant aux utilisateurs d’interrompre la conversation à tout moment.

Ensuite, la fonction ```start``` de gestionnaire initie la conversation (point d'entrée), demandant à l'utilisateur son nom :


```python
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
```

Vous trouverez ici le reste des gestionnaires :

```python
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
        if conn.is_connected():
            cursor.close()
            conn.close()

    return ConversationHandler.END


async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Annule et termine la conversation."""
    await update.message.reply_text(
        'Inscription annulée. À bientôt!',
        reply_markup=ReplyKeyboardRemove()
    )
    return ConversationHandler.END
```

### Fonction ```main``` et sondage du bot

Dans la fonction ```main```, configurez les éléments ```Application``` et ```ConversationHandler```, y compris les points d'entrée, les états et les solutions de secours. Démarrez le bot avec des interrogations pour écouter les mises à jour :

```python
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
```

### Exécutez votre bot :
Complétez votre script en appelant la mainfonction. Exécutez votre bot en exécutant le script Python dans votre terminal.

Vous trouverez ici le code complet :

```python
import logging
from telegram import (ReplyKeyboardMarkup, ReplyKeyboardRemove, Update,
                      InlineKeyboardButton, InlineKeyboardMarkup)
from telegram.ext import (Application, CallbackQueryHandler, CommandHandler,
                          ContextTypes, ConversationHandler, MessageHandler, filters)
from dotenv import load_dotenv
import os
import mysql.connector

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
        if conn.is_connected():
            cursor.close()
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
```

---

## ▶️ 5. Lancer le bot

Après avoir exécuté votre script, recherchez votre bot sur Telegram et commencez à interagir avec lui. Vous devriez maintenant pouvoir utiliser la commande ```/start``` pour démarrer une conversation, qui vous guidera tout au long de la phase d'inscription de l'etudiant.

| | | |
|:---:|:---:|
| ![Image 1](images/image1.webp) | ![Image 2](images/image2.webp) |
| ![Image 3](images/image3.webp) | ![Image 4](images/image4.webp) |
| ![Image 5](images/image5.webp) | ![Image 6](images/image6.webp) |
| ![Image 7](images/image7.webp) | ![Image 8](images/image8.webp) |

# Conclusion:

Vous pouvez étendre votre bot Telegram pour y inclure la gestion des SMS et des boutons interactifs, le rendant ainsi beaucoup plus attrayant. Ce n'est qu'un aperçu des possibilités offertes par la bibliothèque ```python-telegram-bot```. En explorant plus en profondeur, vous découvrirez des options pour gérer différents types de contenu, intégrer des API externes et bien plus encore. Plongez dans la documentation de la bibliothèque pour découvrir toutes les possibilités de votre nouveau bot Telegram.

Bon codage et amusez-vous à donner vie à votre bot Telegram !

---