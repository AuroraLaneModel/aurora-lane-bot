#!/bin/bash
apt update && apt upgrade -y
apt install python3 python3-pip git -y
git clone https://github.com/SEU-USUARIO/aurora-lane-bot.git
cd aurora-lane-bot
pip3 install -r requirements.txt
echo 'INSTALAÇÃO FINALIZADA. COLOQUE SEU BOT_TOKEN NO .env'
