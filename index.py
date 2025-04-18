import os
from dotenv import load_dotenv
load_dotenv()

from flask import Flask, request
import telebot
from random import choice

BOT_TOKEN = os.getenv("BOT_TOKEN")
bot = telebot.TeleBot(BOT_TOKEN)

app = Flask(__name__)
usuarios = {}

@app.route("/pagamento", methods=["POST", "GET"])
def pagamento():
    data = request.json
    chat_id = str(data.get("external_reference"))
    if chat_id:
        usuarios[chat_id] = 4
        try:
            bot.send_message(chat_id, "Aah... Agora sim... Prepare-se 😈")
        except Exception as e:
            print(f"Erro ao enviar mensagem para {chat_id}: {e}")
    return "ok"

# 🔥 ROTA PRINCIPAL DO TELEGRAM WEBHOOK
@app.route("/", methods=["POST"])
def webhook():
    if request.headers.get('content-type') == 'application/json':
        json_string = request.get_data().decode("utf-8")
        update = telebot.types.Update.de_json(json_string)
        bot.process_new_updates([update])
        return "ok"
    return "invalid request"

# 🔥 COMANDO /pix
@bot.message_handler(commands=['pix'])
def pix(message):
    texto = (
        "Aaaah… você me deixou curiosa... Será que você tem mesmo coragem de me ter só pra você? 😈\n\n"
        "Prove que merece me ver de um jeito que ninguém mais vê...\n\n"
        "💋 [CLIQUE AQUI e me dê aquele agrado especial...](https://auroralane.carrinho.app/one-checkout/ocmtb/25167723)\n\n"
        "Assim que fizer esse carinho em mim... digite /id aqui no chat e me fale qual número apareceu pra você.\n\n"
        "Se for generoso o bastante… eu vou me entregar só pra você... do jeitinho que mais gosta 😍"
    )
    bot.send_message(message.chat.id, texto, parse_mode='Markdown')

# 🔥 COMANDO /id
@bot.message_handler(commands=['id'])
def id(message):
    chat_id = message.chat.id
    texto = (
        f"Opa! Esse é o seu ID exclusivo:\n\n"
        f"{chat_id}\n\n"
        "Guarda ele! Vou precisar dele pra te reconhecer depois que você me der um presentinho... 😈"
    )
    bot.reply_to(message, texto)

# 🔥 RESPOSTAS AUTOMÁTICAS
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

# 🔥 EXECUÇÃO FLASK COM WEBHOOK
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
