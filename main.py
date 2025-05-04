import telebot
from telebot import types
import os
from dotenv import load_dotenv
import logging
from enum import Enum
import json
import re

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("bot.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

load_dotenv()
TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN') or "7559909274:AAEj4U6xGXz0PBgXMiFvkNNqbfkiD3OJTJo"
if not TELEGRAM_BOT_TOKEN:
    logger.error("Token do Telegram não encontrado no arquivo .env")
    raise ValueError("Token do Telegram não configurado. Adicione TELEGRAM_BOT_TOKEN ao arquivo .env")

bot = telebot.TeleBot(TELEGRAM_BOT_TOKEN)

USER_DATA_FILE = "user_data.json"

def load_user_data():
    try:
        if os.path.exists(USER_DATA_FILE):
            with open(USER_DATA_FILE, 'r', encoding='utf-8') as file:
                return json.load(file)
        return {}
    except Exception as e:
        logger.error(f"Erro ao carregar dados de usuários: {e}")
        return {}

def save_user_data(data):
    try:
        with open(USER_DATA_FILE, 'w', encoding='utf-8') as file:
            json.dump(data, file, ensure_ascii=False, indent=2)
    except Exception as e:
        logger.error(f"Erro ao salvar dados de usuários: {e}")

user_data = load_user_data()

class MenuOptions(Enum):
    REDES_SOCIAIS = 'redes_sociais'
    LIVES = 'lives'
    PROMOCOES = 'promocoes'
    SOBRE_TIME = 'sobre_time'
    PROXIMOS_JOGOS = 'proximos_jogos'
    NOTICIAS = 'noticias'
    VOLTAR = 'voltar'
    ALTERAR_NOME = 'alterar_nome'

REDES_SOCIAIS_MSG = """FUR {user_name}, nossas redes sociais! 🔥

📷 Instagram: https://www.instagram.com/furiagg
📘 Facebook: https://www.facebook.com/furiagg
▶️ YouTube: https://www.youtube.com/@FURIAgg
🐦 X (Twitter): https://x.com/FURIA"""

LIVES_MSG = """FUR {user_name}, nossas lives oficiais! 🎥
▶️ Twitch: https://www.twitch.tv/furiatv
"""

PROMOCOES_MSG = """FUR {user_name}, promoções exclusivas! 🎁
🛍️ Loja Oficial: https://www.furia.gg
🎟️ Cupons de desconto: use o código FURIA10"""

SOBRE_TIME_MSG = """⚡ Sobre a FURIA ⚡

Fundada em 2017, somos uma das maiores organizações de esports do Brasil!

🏆 Títulos importantes:
- 6x Campeã Brasileira de CS:GO
- 1x Campeã Mundial de Valorant
- 3x Campeã da ESL

📌 Saiba mais: https://www.furia.gg/quem-somos"""

PROXIMOS_JOGOS_MSG = """📅 Próximos Jogos da FURIA 🎮

🗓️ CS:GO - 15/05 vs MIBR
🗓️ Valorant - 18/05 vs LOUD
🗓️ League of Legends - 22/05 vs Pain

📡 Transmissão: https://www.twitch.tv/furiatv

🔔 Ative as notificações para não perder!"""

NOTICIAS_MSG = """📰 Últimas Notícias da FURIA 📢

🔥 Nova contratação no time de CS:GO
🎮 Campeonato internacional marcado para julho
🛒 Novo drop de merchandise na loja

Leia mais: https://x.com/FURIA"""

MENU_PRINCIPAL_MSG = "Escolha uma das opções abaixo:"

def criar_menu_principal():
    markup = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton("📱 Redes sociais", callback_data=MenuOptions.REDES_SOCIAIS.value)
    btn2 = types.InlineKeyboardButton("🎥 Lives oficiais", callback_data=MenuOptions.LIVES.value)
    btn3 = types.InlineKeyboardButton("🛍️ Promoções", callback_data=MenuOptions.PROMOCOES.value)
    btn4 = types.InlineKeyboardButton("⚡ Sobre o Time", callback_data=MenuOptions.SOBRE_TIME.value)
    btn5 = types.InlineKeyboardButton("📅 Próximos Jogos", callback_data=MenuOptions.PROXIMOS_JOGOS.value)
    btn6 = types.InlineKeyboardButton("📰 Notícias", callback_data=MenuOptions.NOTICIAS.value)
    btn7 = types.InlineKeyboardButton("✏️ Alterar Nome", callback_data=MenuOptions.ALTERAR_NOME.value)
    
    markup.row(btn1, btn2)
    markup.row(btn3, btn4)
    markup.row(btn5, btn6)
    markup.row(btn7)
    return markup

def criar_menu_secundario():
    markup = types.InlineKeyboardMarkup()
    btn_voltar = types.InlineKeyboardButton("🔙 Voltar", callback_data=MenuOptions.VOLTAR.value)
    markup.add(btn_voltar)
    return markup

def validar_nome(nome):
    """Valida o nome do usuário, removendo caracteres especiais e limitando tamanho"""
    nome_limpo = re.sub(r'[^\w\s]', '', nome)
    nome_limpo = nome_limpo.strip()[:30]
    return nome_limpo if nome_limpo else None

@bot.message_handler(commands=['start', 'help'])
def start(msg: telebot.types.Message):
    user_id = str(msg.chat.id) 
    mensagem_boas_vindas = (
        "Fala Furioso(a)! Aqui é o contato inteligente da FURIA! 🔥\n\n"
        "Aqui você fica por dentro de tudo sobre o nosso time, jogos, "
        "lives oficiais, promoções e muito mais!"
    )
    
    bot.send_message(user_id, mensagem_boas_vindas)
    
    if user_id in user_data:
        bot.send_message(
            user_id, 
            f"Bem-vindo de volta, FUR {user_data[user_id]}! 🔥\n"
            f"Use /menu para acessar as opções ou /alterarnome para mudar seu nome."
        )
        mostrar_menu_principal(user_id)
    else:
        bot.send_message(user_id, "Para começar, me diga seu nome!")
        bot.register_next_step_handler(msg, get_name)

@bot.message_handler(commands=['menu'])
def comando_menu(msg: telebot.types.Message):
    user_id = str(msg.chat.id)
    if user_id in user_data:
        mostrar_menu_principal(user_id)
    else:
        bot.send_message(user_id, "Primeiro preciso saber seu nome. Digite /start para começar.")

@bot.message_handler(commands=['alterarnome'])
def comando_alterarnome(msg: telebot.types.Message):
    user_id = str(msg.chat.id)
    bot.send_message(user_id, "Digite seu novo nome:")
    bot.register_next_step_handler(msg, get_name)

def get_name(msg: telebot.types.Message):
    user_name = msg.text.strip()
    user_id = str(msg.chat.id)
    
    nome_validado = validar_nome(user_name)
    
    if not nome_validado:
        bot.send_message(user_id, "Por favor, envie um nome válido (até 30 caracteres, sem caracteres especiais)")
        return bot.register_next_step_handler(msg, get_name)
    
    is_new_user = user_id not in user_data
    
    user_data[user_id] = nome_validado
    save_user_data(user_data) 
    
    if is_new_user:
        bot.send_message(user_id, f"Prazer em te conhecer, FUR {nome_validado}! 🔥")
    else:
        bot.send_message(user_id, f"Nome atualizado com sucesso, FUR {nome_validado}! 🔥")
    
    mostrar_menu_principal(user_id)

def mostrar_menu_principal(user_id):
    try:
        bot.send_message(user_id, MENU_PRINCIPAL_MSG, reply_markup=criar_menu_principal())
    except Exception as e:
        logger.error(f"Erro ao mostrar menu principal: {e}")
        bot.send_message(user_id, "Ocorreu um erro ao exibir o menu. Tente novamente.")

@bot.callback_query_handler(func=lambda call: True)
def handle_menu_selection(call):
    user_id = str(call.message.chat.id)
    user_name = user_data.get(user_id, "Furioso(a)")
    
    try:
        option = MenuOptions(call.data)
        
        if option == MenuOptions.VOLTAR:
            bot.answer_callback_query(call.id)
            mostrar_menu_principal(user_id)
            return
        
        if option == MenuOptions.ALTERAR_NOME:
            bot.answer_callback_query(call.id)
            bot.send_message(user_id, "Digite seu novo nome:")
            bot.register_next_step_handler(call.message, get_name)
            return
        
        if option == MenuOptions.REDES_SOCIAIS:
            resposta = REDES_SOCIAIS_MSG.format(user_name=user_name)
        elif option == MenuOptions.LIVES:
            resposta = LIVES_MSG.format(user_name=user_name)
        elif option == MenuOptions.PROMOCOES:
            resposta = PROMOCOES_MSG.format(user_name=user_name)
        elif option == MenuOptions.SOBRE_TIME:
            resposta = SOBRE_TIME_MSG
        elif option == MenuOptions.PROXIMOS_JOGOS:
            resposta = PROXIMOS_JOGOS_MSG
        elif option == MenuOptions.NOTICIAS:
            resposta = NOTICIAS_MSG
        else:
            resposta = "Opção inválida. Selecione uma opção do menu."

        try:
            bot.answer_callback_query(call.id)
            
            bot.edit_message_text(
                chat_id=user_id,
                message_id=call.message.message_id,
                text=resposta,
                reply_markup=criar_menu_secundario(),
                disable_web_page_preview=False 
            )
        except telebot.apihelper.ApiTelegramException as e:
            if "message is not modified" in str(e):
                pass
            else:
                logger.warning(f"Erro ao editar mensagem: {e}")
                bot.send_message(user_id, resposta, reply_markup=criar_menu_secundario())

    except ValueError:
        logger.warning(f"Opção inválida recebida: {call.data}")
        bot.answer_callback_query(call.id, "Opção inválida!")
    except Exception as e:
        logger.error(f"Erro inesperado: {e}")
        bot.answer_callback_query(call.id, "Ocorreu um erro. Tente novamente.")
        mostrar_menu_principal(user_id)

@bot.message_handler(func=lambda message: True)
def handle_all_messages(message):
    """Manipula todas as mensagens que não correspondem a comandos definidos"""
    user_id = str(message.chat.id)
    

    if user_id in user_data:
        bot.send_message(
            user_id, 
            "Use os botões abaixo para navegar pelo menu da FURIA:",
            reply_markup=criar_menu_principal()
        )
    else:
        bot.send_message(
            user_id,
            "Olá! Para começar a usar o bot da FURIA, preciso saber seu nome. Digite /start para começar."
        )

if __name__ == '__main__':
    logger.info("Bot da FURIA iniciando...")
    try:
        bot.infinity_polling(timeout=10, long_polling_timeout=5)
    except Exception as e:
        logger.critical(f"Erro crítico no bot: {e}")