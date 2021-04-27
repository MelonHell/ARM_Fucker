import json
import os
import random
import subprocess
import time
import webbrowser

from chromote import Chromote

import scripts

# SETTINGS
configFileName = "ARM_Fucker.json"


def log(text):
    print(f"[{time.strftime('%H:%M:%S')}] {text}")


def sendPacket(packet_name, data):
    tab.evaluate(f'DS.util.websocket.send("{packet_name}", {data})')


def console(text):
    split = text.split(" ")
    cmd = split[0].lower()
    args = split[1:]
    if cmd == "help":
        log("dbg - открыть браузер с деббагером")
        log("js - выполнить js скрипт")
        log("chat <текст> - отправить сообщение в чат")
        log("packet <название пакета> <json данные> - отправить пакет")
        log("theme - применить тему")
    elif cmd == "dbg":
        url = f"http://localhost:{port}"
        log("Запуск браузера, если не работает, то ссылка: " + url)
        webbrowser.open(url)
    elif cmd == "js":
        tab.evaluate(" ".join(args))
    elif cmd == "chat":
        msg = " ".join(args)
        sendPacket("addChatMessage", f'"{msg}"')
        log("Сообщение отправлено")
    elif cmd == "packet":
        if len(args) >= 2:
            packet_name = args[0]
            data = " ".join(args[1:])
            sendPacket(packet_name, data)
            log("Пакет отправлен")
        else:
            log("packet <название пакета> <json данные> - отправить пакет")
    elif cmd == "theme":
        tab.evaluate(scripts.insertCss)
        log("Тема применена")
    else:
        log("Команда не найдена")


def main():
    print(
        ' ______     ______     __    __     ______   __  __     ______     __  __     ______     ______    \n/\\  __ \\   /\\  == \\   /\\ "-./  \\   /\\  ___\\ /\\ \\/\\ \\   /\\  ___\\   /\\ \\/ /    /\\  ___\\   /\\  == \\   \n\\ \\  __ \\  \\ \\  __<   \\ \\ \\-./\\ \\  \\ \\  __\\ \\ \\ \\_\\ \\  \\ \\ \\____  \\ \\  _"-.  \\ \\  __\\   \\ \\  __<   \n \\ \\_\\ \\_\\  \\ \\_\\ \\_\\  \\ \\_\\ \\ \\_\\  \\ \\_\\    \\ \\_____\\  \\ \\_____\\  \\ \\_\\ \\_\\  \\ \\_____\\  \\ \\_\\ \\_\\ \n  \\/_/\\/_/   \\/_/ /_/   \\/_/  \\/_/   \\/_/     \\/_____/   \\/_____/   \\/_/\\/_/   \\/_____/   \\/_/ /_/ \n ______     __  __    \n/\\  == \\   /\\ \\_\\ \\   \n\\ \\  __<   \\ \\____ \\  \n \\ \\_____\\  \\/\\_____\\ \n  \\/_____/   \\/_____/ \n __    __     ______     __         ______     __   __     __  __     ______     __         __        \n/\\ "-./  \\   /\\  ___\\   /\\ \\       /\\  __ \\   /\\ "-.\\ \\   /\\ \\_\\ \\   /\\  ___\\   /\\ \\       /\\ \\       \n\\ \\ \\-./\\ \\  \\ \\  __\\   \\ \\ \\____  \\ \\ \\/\\ \\  \\ \\ \\-.  \\  \\ \\  __ \\  \\ \\  __\\   \\ \\ \\____  \\ \\ \\____  \n \\ \\_\\ \\ \\_\\  \\ \\_____\\  \\ \\_____\\  \\ \\_____\\  \\ \\_\\\\"\\_\\  \\ \\_\\ \\_\\  \\ \\_____\\  \\ \\_____\\  \\ \\_____\\ \n  \\/_/  \\/_/   \\/_____/   \\/_____/   \\/_____/   \\/_/ \\/_/   \\/_/\\/_/   \\/_____/   \\/_____/   \\/_____/ \n')
    log("ARM_Fucker by MelonHell запущен")
    global port, chrome
    port = random.randint(1000, 9999)
    log(f"Порт дебаггера: {port}")

    login_data = None

    try:
        with open(configFileName, "r") as f:
            jsonData = json.load(f)
            if "login" in jsonData and "password" in jsonData:
                log("Обнаружен сохранёный пароль. Автоматическая авторизация")
                login = jsonData["login"]
                password = jsonData["password"]
                login_data = login, password
    except:
        pass

    use_theme = input("Хош ахуеную кастомную тему? Y/n: ")

    if os.path.exists("ARM_Student.exe"):
        subprocess.Popen(f"ARM_Student.exe --remote-debugging-port={port}")
    elif os.path.exists("ARM_Student/ARM_Student.exe"):
        subprocess.Popen(f"ARM_Student/ARM_Student.exe --remote-debugging-port={port}")
    else:
        log("Авроры нэма чёт, закинь эту хуйню в папку с авророй")
        time.sleep(5)
        return;

    # WAIT AVRORA
    isStarted = False
    for i in range(10):
        if isStarted:
            continue
        log(f"Ожидание запуска этой поеботы. Попытка {i + 1} из 10")
        try:
            chrome = Chromote(port=port)
            isStarted = True
        except:
            pass
    if not isStarted:
        log("ОШИБКА! Аврора не запустилась. Завершение скрипта")
        return
    log("Заебись! Вроде запустилось")
    global tab
    tab = chrome.tabs[0]

    for i in range(100):
        if login_data is not None:
            continue
        log("Ожидание входа")
        tab.evaluate(scripts.buttonJs)
        att_idUser = json.loads(tab.evaluate(scripts.getIdUser))
        att_password = json.loads(tab.evaluate(scripts.getPassword))
        if att_idUser['result']['result']['type'] == 'string' and att_password['result']['result']['type'] == 'string':
            login = att_idUser['result']['result']['value']
            password = att_password['result']['result']['value']
            login_data = login, password
            with open(configFileName, "w") as f:
                json.dump({"login": login, "password": password}, f)
            log("Пароль сохранён")

    log("Авторизация")
    tab.set_url(f"https://mirea2.aco-avrora.ru/student/?ArmUserId={login_data[0]}&ArmUserPassword={login_data[1]}")

    log("Ждем 5 сек")
    time.sleep(5)
    log("Выполнение основного скрипта")
    tab.evaluate(scripts.mainScript)
    if use_theme in ["", "Y", "y", "1"]:
        log("Применяем мою ахуительную тему")
        tab.evaluate(scripts.insertCss)
    log("АХУЕТЬ ОНО РАБОТАЕТ! Наверное..")
    log("Переход в режим консоли, если она тебе нахуй не нужна, можешь смело закрывать эту хуйню")
    while True:
        console(input("> "))


if __name__ == '__main__':
    main()
