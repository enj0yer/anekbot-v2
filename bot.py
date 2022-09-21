import types

import sqlite3
from telebot import *


bot = telebot.TeleBot


# Получение одного случайного анекдота из базы данных
def getData() -> str:
    con = sqlite3.connect(path)
    cur = con.cursor()
    res = cur.execute(
        "SELECT * FROM anekdots LIMIT 1 OFFSET abs(random() % (select count(*) from anekdots));").fetchone()
    con.close()
    return res


# Добавление анекдота в базу данных
def setData(data):
    con = sqlite3.connect(path)
    cur = con.cursor()
    cur.execute("INSERT INTO anekdots VALUES (?)", (data.text,))
    con.commit()
    con.close()


# Получение всего списка анекдотов (для отладки)
def getAll() -> list:
    con = sqlite3.connect(path)
    cur = con.cursor()
    res = cur.execute("SELECT * FROM anekdots").fetchall()
    con.close()
    return res


# Получение анекдота из таблицы для администрирования
def getUsernameForAdmin() -> str:
    con = sqlite3.connect(path)
    cur = con.cursor()
    res = cur.execute("SELECT user_id FROM admin LIMIT 1").fetchone()
    con.close()
    return res


# Получение анекдота для администрирования
def getTextForAdmin() -> str:
    con = sqlite3.connect(path)
    cur = con.cursor()
    res = cur.execute("SELECT text FROM admin LIMIT 1").fetchone()
    con.close()
    return res


# Добавление анекдота в таблицу для администрирования
def addToAdmin(data):
    con = sqlite3.connect(path)
    cur = con.cursor()
    cur.execute("INSERT INTO admin VALUES (?, ?)", (data.from_user.id, data.text,))
    con.commit()
    con.close()


# Удаление анекдота из таблицы администрирования
def deleteByAdmin(data):
    con = sqlite3.connect(path)
    cur = con.cursor()
    user_id = cur.execute(f"SELECT user_id FROM admin WHERE text = '{data.text}'").fetchone()
    cur.execute(f"DELETE FROM admin WHERE user_id = '{user_id[0]}'")
    con.commit()
    con.close()
    bot.send_message(user_id[0], "Ваш анекдот не был добавлен")


# Добавление анекдота из таблицы администрирования в основную таблицу
def addByAdmin(data):
    con = sqlite3.connect(path)
    cur = con.cursor()
    user_id = cur.execute(f"SELECT user_id FROM admin WHERE text = '{data.text}'").fetchone()
    cur.execute(f"DELETE FROM admin WHERE user_id = '{user_id[0]}'")
    con.commit()
    cur.execute("INSERT INTO anekdots VALUES (?)", (data.text,))
    con.commit()
    con.close()
    bot.send_message(user_id[0], "Ваш анекдот был успешно добавлен")


#

# Получение списка забаненых пользователей
# def getBanList():
#     con = sqlite3.connect(path)
#     cur = con.cursor()
#     var_res = cur.execute("SELECT user_id FROM ban_list").fetchall()
#     res = var_res
#     for i in range(len(res)):
#         var_res = cur.execute(f"SELECT username FROM all_users WHERE user_id = '{res[i]}'").fetchone()
#         if (var_res != None):
#             res[i].append(var_res)
#     con.close()
#     return res

# Заблокирование пользователя
def banUser(user_id):
    con = sqlite3.connect(path)
    cur = con.cursor()
    cur.execute(f"INSERT OR IGNORE INTO ban_list VALUES (?)", (user_id,))
    con.commit()
    con.close()


# Проверка пользователя на наличие в бан листе
def checkBan(user_id) -> bool:
    con = sqlite3.connect(path)
    cur = con.cursor()
    res = cur.execute(f"SELECT user_id FROM ban_list WHERE user_id = '{user_id}'").fetchall()
    con.close()
    if (len(res) == 0):
        return False
    return True


# Разблокирование пользователя
def unbanUser(user_id):
    con = sqlite3.connect(path)
    cur = con.cursor()
    cur.execute(f"DELETE FROM ban_list WHERE user_id = '{user_id}'")
    con.commit()
    con.close()


def addToList(user_id, username):
    con = sqlite3.connect(path)
    cur = con.cursor()
    cur.execute(f"INSERT OR IGNORE INTO all_users VALUES (?, ?)", (user_id, username,))
    con.commit()
    con.close()


@bot.message_handler(commands=['start'])
def starting(message):
    if (checkBan(message.from_user.id)):
        bot.send_message(message.from_user.id, "Вы были забанены")
    else:
        addToList(message.from_user.id, message.from_user.username)
        bot.send_message(message.from_user.id,
                         f"Приветствую, {message.from_user.username}, самое время для разрывного анекдота? Для получения анекдота пишите /rzhaka или нажмите на кнопку внизу сообщения.\nЕсли желаете добавить анекдот в список, то просто отправьте его боту, админ проверит анекдот и бот отправит вам результат проверки.")
        print(message.from_user, message.text, sep="\t")


@bot.message_handler(commands=['rzhaka'])
def send_anek(message):
    if (checkBan(message.from_user.id)):
        bot.send_message(message.from_user.id, "Вы были забанены")
    else:
        anekdot = getData()
        bot.send_message(message.from_user.id, anekdot)
        print(message.from_user, message.text, anekdot, sep="\t")


@bot.message_handler(commands=['all'])
def send_all(message):
    if (message.from_user.id == ADMINID):
        listForAll = getAll()
        for i in listForAll:
            bot.send_message(message.from_user.id, i)


# @bot.message_handler(commands=['banlist'])
# def check_ban_list(message):
#     if (message.from_user.id == ADMINID):
#         banList = getBanList()
#         if (banList == []):
#             bot.send_message(ADMINID, "Список заблокированных пользователей пустой")
#         else:
#             res = ""
#             for i in range(len(banList)):
#                 res += str(banList[i][0]) + " " + banList[i][1] + "\n"
#             bot.send_message(ADMINID, res)


def check(text) -> bool:
    if (
            text != "/ban" and text != "/unban" and text != "/tell" and text != "/start" and text != "/rzhaka" and text != "/all" and text != "/banlist" and text != "/admin" and text != ""):
        return True
    return False


@bot.message_handler(commands=['admin'])
def check_admin_list(message):
    if (message.from_user.id == ADMINID):
        user_id = getUsernameForAdmin()
        if (user_id == None):
            bot.send_message(message.from_user.id, "Список администрирования пуст")
        else:
            keyboard = types.InlineKeyboardMarkup()
            buttonTrue = types.InlineKeyboardButton(text="Добавить", callback_data="isTrue")
            buttonFalse = types.InlineKeyboardButton(text="Не добавлять", callback_data="isFalse")
            keyboard.add(buttonTrue, buttonFalse, row_width=1)
            bot.send_message(message.from_user.id, getTextForAdmin(), reply_markup=keyboard)


@bot.message_handler(content_types=['text'])
def write_anek(message):
    parsedStr = message.text.split(" ")
    if (message.from_user.id == ADMINID and parsedStr[0] == "/tell"):
        messageToUser = ""
        for i in range(2, len(parsedStr)):
            messageToUser += parsedStr[i] + " "
        bot.send_message(int(parsedStr[1]), messageToUser)
    if (message.from_user.id == ADMINID and parsedStr[0] == "/ban"):
        messageToUser = ""
        for i in range(2, len(parsedStr)):
            messageToUser += parsedStr[i] + " "
        bot.send_message(int(parsedStr[1]), "Вы были забанены по причине: " + messageToUser)
        banUser(int(parsedStr[1]))
    if (message.from_user.id == ADMINID and parsedStr[0] == "/unban"):
        messageToUser = ""
        for i in range(2, len(parsedStr)):
            messageToUser += parsedStr[i] + " "
        bot.send_message(int(parsedStr[1]), "Вы были разбанены со словами: " + messageToUser)
        unbanUser(int(parsedStr[1]))

    if message.from_user.id == ADMINID and check(parsedStr[0]) and check(message.text):
        setData(message)
        print(message.from_user, message.text, sep="\t")
    if (message.from_user.id != ADMINID and check(parsedStr[0]) and check(message.text)):
        if (checkBan(message.from_user.id)):
            bot.send_message(message.from_user.id, "Вы были забанены")
        else:
            addToAdmin(message)
            print(message.from_user, message.text, sep="\t")
            bot.send_message(message.from_user.id, "Ваш анекдот на рассмотрении")


@bot.callback_query_handler(func=lambda call: True)
def admin_choice(call):
    if (call.data == "isTrue"):
        addByAdmin(call.message)
    if (call.data == "isFalse"):
        deleteByAdmin(call.message)


bot.polling(non_stop=True, interval=0)
