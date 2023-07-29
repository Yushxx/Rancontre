from flask import Flask, request
from telegram import Update, ForceReply
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, ConversationHandler, CallbackContext
import random
import sqlite3

# Replace "YOUR_TELEGRAM" with the actual token
TOKEN = "6363609133:AAGokjYGa80BOoeG2ItLOiEA6_TYaFEKc60"

app = Flask(__name__)

# Database connection function
def get_db_connection():
    conn = sqlite3.connect('profiles.db')
    conn.row_factory = sqlite3.Row
    return conn

# Command handlers
def start(update: Update, _: CallbackContext) -> int:
    user = update.message.from_user
    update.message.reply_text(f"Bonjour {user.first_name} ! Bienvenue sur le bot de rencontres. "
                              "Utilisez la commande /create_profile pour créer votre profil.")
    return ConversationHandler.END

def create_profile(update: Update, _: CallbackContext) -> int:
    update.message.reply_text("Pour créer votre profil, veuillez saisir votre nom:")
    return 1

def get_name(update: Update, _: CallbackContext) -> int:
    user = update.message.from_user
    name = update.message.text
    # You can save the name in the database here
    update.message.reply_text(f"Merci {name} ! Quel est votre âge ?")
    return 2

def get_age(update: Update, _: CallbackContext) -> int:
    age = update.message.text
    # You can save the age in the database here
    update.message.reply_text("Quel est votre genre ?")
    return 3

def get_gender(update: Update, _: CallbackContext) -> int:
    gender = update.message.text
    # You can save the gender in the database here
    update.message.reply_text("Veuillez télécharger votre photo de profil (URL) :")
    return 4

def get_photo(update: Update, _: CallbackContext) -> int:
    photo = update.message.text
    # You can save the photo URL in the database here
    update.message.reply_text("Votre profil a été créé avec succès ! "
                              "Utilisez la commande /find_partner pour trouver un partenaire.")
    return ConversationHandler.END

def find_partner(update: Update, _: CallbackContext):
    conn = get_db_connection()
    profiles = conn.execute('SELECT * FROM profiles').fetchall()
    conn.close()

    if len(profiles) < 2:
        update.message.reply_text("Désolé, il n'y a pas assez de profils pour trouver un partenaire.")
    else:
        partner1, partner2 = random.sample(profiles, 2)
        update.message.reply_text(f"Voici votre partenaire 1 : {partner1['name']} ({partner1['gender']}, {partner1['age']} ans).")
        update.message.reply_text(f"Voici votre partenaire 2 : {partner2['name']} ({partner2['gender']}, {partner2['age']} ans).")

    return ConversationHandler.END

def main():
    updater = Updater(TOKEN)
    dispatcher = updater.dispatcher

    # Command handlers
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(ConversationHandler(
        entry_points=[CommandHandler("create_profile", create_profile)],
        states={
            1: [MessageHandler(Filters.text & ~Filters.command, get_name)],
            2: [MessageHandler(Filters.text & ~Filters.command, get_age)],
            3: [MessageHandler(Filters.text & ~Filters.command, get_gender)],
            4: [MessageHandler(Filters.text & ~Filters.command, get_photo)]
        },
        fallbacks=[],
    ))
    dispatcher.add_handler(CommandHandler("find_partner", find_partner))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
