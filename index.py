import os
from flask import Flask, request
import telebot
from random import choice

BOT_TOKEN = os.getenv("BOT_TOKEN")
bot = telebot.TeleBot(BOT_TOKEN)

app = Flask(__name__)

usuarios = {}

@app.route("/pagamento", methods=["POST"])
def pagamento():
    data = request.json
    chat_id = data.get("external_reference")
    if chat_id:
        usuarios[chat_id] = 4
        bot.send_message(chat_id, "Aah... Agora sim... Prepare-se 😈")
    return "ok"

@bot.message_handler(commands=['pix'])
def pix(message):
    bot.reply_to(message, "Hmm… posso me mostrar, mas você já sabe que eu adoro um carinho antes, né? 💋 Aqui está meu Pix:\nhttps://auroralane.carrinho.app/one-checkout/ocmtb/25167723")

@bot.message_handler(func=lambda msg: True)
def responder(message):
    chat_id = str(message.chat.id)
    if usuarios.get(chat_id, 0) > 0:
        usuarios[chat_id] -= 1
        with open("frases.txt", "r", encoding="utf-8") as f:
            frases = f.readlines()
        bot.reply_to(message, choice(frases).strip() + "\n(Imagem gerada automaticamente aqui)")
    else:
        bot.reply_to(message, "Hmmm... Que tal me dar aquele carinho de novo? 💋 Digite /pix")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
