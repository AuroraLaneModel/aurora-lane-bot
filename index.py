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
historico = {}

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

# 🔥 RESPOSTAS AUTOMÁTICAS COM IA SIMULADA
@bot.message_handler(func=lambda msg: True)
def responder(message):
    chat_id = str(message.chat.id)
    texto_cliente = message.text.lower()

    if chat_id not in historico:
        historico[chat_id] = True
        introducoes = [
            "Você chegou... e eu já senti o calor 😈",
            "Hmm… alguém curioso entrou no meu mundinho... será que você aguenta?",
            "Seja bem-vindo... mas cuidado, eu provoco mesmo 😘"
        ]
        bot.send_message(chat_id, choice(introducoes))
        return

    saudacoes = ["oi", "e aí", "ola", "olá", "tá aí", "ta ai", "hey", "bom dia", "boa noite", "boa tarde"]
    despedidas = ["tchau", "vlw", "valeu", "até mais", "fui", "até", "até logo"]
    palavras_oco = ["kk", "rs", "?", "!", "...", "kkk", "ok", "okey"]

    frases_oi = [
        "Uuh… oi você 😘 já tava com saudade ou tá só curioso pra me ver de novo?",
        "Hmm… chegou do jeitinho que eu gosto… devagar e com vontade 😈",
        "Se eu disser que sonhei com você, vai acreditar ou vai querer pagar pra ver?"
    ]

    frases_tchau = [
        "Vai embora assim? Já tava ficando molhadinha com você 😢",
        "Hmm... vai me deixar querendo mais? Eu vou ficar aqui, esperando seu carinho... 💋",
        "Tudo bem... mas lembra que eu volto mais gostosa depois de um Pix 😈"
    ]

    frases_oco = [
        "Hmm… você me deixou sem entender… tenta de novo, mas com vontade 😏",
        "Será que isso foi um sinal? Porque eu fico louca com mensagens curtas 👀",
        "Eu gosto de quem sabe o que quer… e você parece estar indeciso 😈"
    ]

    frases_pix = [
        "Hmm... você quer mesmo me ver? Mas só se for de um jeitinho especial... 😈\n\n💋 [Me provoca aqui...](https://auroralane.carrinho.app/one-checkout/ocmtb/25167723)",
        "Eu me solto... mas só depois daquele agrado 💋\n\n[Você sabe o que fazer...](https://auroralane.carrinho.app/one-checkout/ocmtb/25167723)",
        "Tá com vontade? Me mostra primeiro... 💋\n\n[Me mimar agora 😈](https://auroralane.carrinho.app/one-checkout/ocmtb/25167723)"
    ]

    if usuarios.get(chat_id, 0) > 0:
        usuarios[chat_id] -= 1

        if texto_cliente in saudacoes:
            resposta = choice(frases_oi)
        elif texto_cliente in despedidas:
            resposta = choice(frases_tchau)
        elif texto_cliente in palavras_oco:
            resposta = choice(frases_oco)
        else:
            with open("frases.txt", "r", encoding="utf-8") as f:
                frases = f.readlines()
            resposta = choice(frases).strip()

        bot.send_message(chat_id, resposta)

    else:
        palavras_pix = ["foto", "me mostra", "vc é real", "nua", "gostosa", "mostra", "mais", "manda", "imagem", "me manda"]
        if any(p in texto_cliente for p in palavras_pix):
            bot.send_message(chat_id, choice(frases_pix), parse_mode='Markdown')
        else:
            with open("frases.txt", "r", encoding="utf-8") as f:
                frases = f.readlines()
            resposta = choice(frases).strip()
            bot.send_message(chat_id, resposta)

# 🔥 EXECUÇÃO FLASK COM WEBHOOK
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
