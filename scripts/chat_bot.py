import telebot

from environment_variables import TELEGRAM_API_KEY, CONTACT_EMAIL, ASSINATURA_LINK, PROPAGA_FEEDBACK_CHAT_ID

bot = telebot.TeleBot(TELEGRAM_API_KEY)

state = None
login = None
password = None


def enviar_mensagem_padrao(message):
    text = "Desculpe não entendi o que você digitou, volte para o /menu"
    bot.reply_to(message, text)


@bot.message_handler(commands=["start", "menu"])
def menu(message):
    print(message)
    text = "Olá selecione a opção desejada para continuar:" \
           "\n /feedback Nos de um feedback sobre o nosso produto" \
           "\n /adquirir_assinatura Adquira uma assinatura do nosso produto" \
           "\n /cancelar_assinatura Cancele sua Assinatura" \
           "\n /fale_conosco Entre em contato com um de nossos especialistas" \
           "\nPor favor clique em uma das opções, digitar outra coisa não irá funcionar."
    bot.send_message(message.chat.id, text)


@bot.message_handler(commands=["feedback"])
def feedback(message):
    global state
    texto = "Porfavor, digite o seu feedback"
    bot.send_message(message.chat.id, texto)
    state = "feedback"


def receive_feedback(message, chat_id_list: list = PROPAGA_FEEDBACK_CHAT_ID):
    global state
    state = None
    text = "Obrigado pelo seu feedback"
    bot.send_message(message.chat.id, text)
    for chat_id in chat_id_list:
        feedback_text = f"Foi enviado um feedback pelo telegram, O conteúdo do feedback é:\n{message.text}"
        bot.send_message(chat_id, feedback_text)


@bot.message_handler(commands=["adquirir_assinatura"])
def adquirir_assinatura(message):
    text = f"Para adquirir uma assinatura do nosso produto acesse o link: {ASSINATURA_LINK}"
    bot.send_message(message.chat.id, text)


@bot.message_handler(commands=["cancelar_assinatura"])
def cancelar_assinatura(message):
    global state
    state = "cancelar_assinatura_menu"
    text = f"Por favor selecione a maneira que deseja se autenticar para cancelar sua assinatura:" \
           f"\n    /product_key Possuo meu product key" \
           f"\n    /login_password Possuo meu login e senha" \
           f"\nResponder com qualquer outra coisa não irá funcionar, por favor clique em uma das opções"
    bot.send_message(message.chat.id, text)


@bot.message_handler(commands=["product_key"])
def cancelar_assinatura_product_key_option(message):
    global state
    if state == "cancelar_assinatura_menu":
        text = f"Por favor digite apenas o seu product key sem espaços em uma única linha:"
        bot.send_message(message.chat.id, text)
        state = "cancelar_assinatura_step_product_key"
    else:
        enviar_mensagem_padrao(message)


# TODO validar product key do usuario
def valida_product_key(message):
    if message.text == '123':
        return True
    else:
        return False


def cancelar_assinatura_product_key(message):
    global state
    state = None
    if valida_product_key(message):
        text = "Product key valido, sua assinatura foi cancelada"
        bot.send_message(message.chat.id, text)
    else:
        text = "Product key invalido, não foi possível cancelar a sua assinatura"
        bot.send_message(message.chat.id, text)


@bot.message_handler(commands=["login_password"])
def cancelar_assinatura_login_password_option(message):
    global state
    if state == "cancelar_assinatura_menu":
        text = f"Por favor digite apenas o seu email, sem espaços, em uma única linha:"
        bot.send_message(message.chat.id, text)
        state = "cancelar_assinatura_step_login"
    else:
        enviar_mensagem_padrao(message)


# TODO validar login e password do usuario
def valida_login_password(email, pwd):
    if email == "email" and pwd == "senha":
        return True
    else:
        return False


def cancelar_assinatura_login_password(message):
    global login
    global state
    global password

    if state == "cancelar_assinatura_step_login":
        login = message.text
        text = f"Por favor digite apenas o seu password, sem espaços, em uma única linha:"
        bot.send_message(message.chat.id, text)
        state = "cancelar_assinatura_step_password"
    elif state == "cancelar_assinatura_step_password":
        pwd = message.text
        if valida_login_password(login, pwd):
            text = "Autenticação válida, sua assinatura foi cancelada"
            bot.send_message(message.chat.id, text)
        else:
            text = "Autenticação inválida, não foi possível cancelar a sua assinatura"
            bot.send_message(message.chat.id, text)
        state = None
        login = None
        password = None


@bot.message_handler(commands=["fale_conosco"])
def fale_conosco(message):
    text = f"Para entrar em contato conosco, por favor envie um e-mail para: {CONTACT_EMAIL}"
    bot.send_message(message.chat.id, text)


@bot.message_handler(func=lambda x: True)
def final_message(message):
    global state
    if state == "feedback":
        receive_feedback(message)
    elif state == "cancelar_assinatura_step_product_key":
        cancelar_assinatura_product_key(message)
    elif state in ["cancelar_assinatura_step_login", "cancelar_assinatura_step_password"]:
        cancelar_assinatura_login_password(message)
    else:
        enviar_mensagem_padrao(message)


bot.polling()
