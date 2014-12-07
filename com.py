# coding: utf-8
import serial
import time
import os
from Tkinter import *
from ttk import *
from tkFileDialog import askopenfilename

PORTS_DIR = '/dev/pts/'
BAUDRATES = (50, 75, 110, 134, 150, 200, 300, 600, 1200, 1800, 2400, 4800,
             9600, 19200, 38400, 57600, 115200)
# TIMEOUTS = (0.5, 1, 1.5, 2, 2.5, 3)


def push_to_log(log_obj, message):
    log_obj.insert(END, '')
    log_obj.insert(END, message)


def read_port(event):
    pb['value'] = 0
    port = PORTS_DIR + port_name.get()
    baudrate = int(speed.get())
    # timeout_time = float(timeout.get())

    pb['value'] = 5

    s = serial.Serial(port, baudrate=baudrate, timeout=0.1)
    s.flushInput()  # почистим буфер
    push_to_log(log, 'порт готов')

    pb['value'] = 10

    while True:
        k = s.readline()
        if k == '<<START>>':
            break
    time.sleep(1)

    pb['value'] = 20

    file_name = s.readline().strip()
    print file_name, '<---- name of file'
    push_to_log(log, 'имя принятого файла: %s' % file_name)

    pb['value'] = 30

    # time.sleep(1)
    file_size = s.readline().strip()
    print file_size, '<---- size of file'
    push_to_log(log, 'размер принятого файла: %s bites' % file_size)
    # time.sleep(1)

    pb['value'] = 40
    # content = ''.join(s.readlines())
    data = []
    while s.inWaiting():
        data.append(s.read(1))
    content = ''.join(data)
    push_to_log(log, 'передача окончена')

    pb['value'] = 75

    output_file = open(os.path.join('folder', file_name), 'w')
    output_file.write(content)
    output_file.close()
    push_to_log(log, 'данные записаны в файл')

    pb['value'] = 95
    s.close()  # закрываем за собой КОМ-порт
    pb['value'] = 100


def send_file_via_port(event):
    pb['value'] = 0

    port = PORTS_DIR + port_name.get()
    baudrate = int(speed.get())
    # timeout_time = float(timeout.get())

    pb['value'] = 10

    s = serial.Serial(port, baudrate=baudrate)
    s.flushOutput()  # почистим буфер

    pb['value'] = 20

    path_to_file = askopenfilename()
    with open(path_to_file) as input_file:
        full_file_name = input_file.name
        file_size = os.path.getsize(path_to_file)
        content = input_file.read()

    pb['value'] = 40

    push_to_log(log, 'Начало передачи')
    s.write('<<START>>')
    time.sleep(1)

    pb['value'] = 55

    short_name = full_file_name.split('/')[-1]
    push_to_log(log, 'отправка имени(%s)' % short_name)
    s.write(short_name + '\n')
    # time.sleep(1)

    push_to_log(log, 'отправка размера файла(%d bites)' % file_size)
    s.write(str(file_size) + '\n')
    # time.sleep(1)

    pb['value'] = 65

    push_to_log(log, 'передача содержания файла...')
    # s.write(content)
    for byte in content:
        s.write(byte)
    push_to_log(log, 'передача окончена')

    pb['value'] = 95

    s.close()  # закрываем за собой КОМ-порт

    pb['value'] = 100


root = Tk()
root.title('Соединение COM-портов')

row0 = Frame(root)
row0.pack(side=TOP, fill=X)

# define input port name
row1 = Frame(root)
port_label = Label(row1, width=15, text='Порт:')

ports = os.listdir(PORTS_DIR)
port_name = Combobox(row1, values=ports, height=10)
try:
    port_name.set(ports[0])
except IndexError:
    pass

row1.pack(side=TOP, fill=X)
port_label.pack(side=LEFT)
port_name.pack(side=RIGHT, expand=YES, fill=X)

# define input BAUDRATE
row2 = Frame(root)
speed_label = Label(row2, width=15, text='Скорость:')
speed = Combobox(row2, values=BAUDRATES, height=10)
speed.set(9600)

row2.pack(side=TOP, fill=X)
speed_label.pack(side=LEFT)
speed.pack(side=RIGHT, expand=YES, fill=X)

# # define input timeouts
# row3 = Frame(root)
# timeout_label = Label(row3, width=15, text='Таймаут чтения:')
# timeout = Combobox(row3, values=TIMEOUTS, height=4)
# try:
# timeout.set(TIMEOUTS[0])
# except IndexError:
# timeout.set(0.5)
#
# row3.pack(side=TOP, fill=X)
# timeout_label.pack(side=LEFT)
# timeout.pack(side=RIGHT, expand=YES, fill=X)


# define buttons
row4 = Frame(root)
btn_read = Button(row4, text='Прослушивать порт', command=(lambda: read_port(None)))
btn_read.pack(side=LEFT, expand=YES, fill=X)

row4.pack(side=TOP, fill=X)
btn_write = Button(row4, text='Послать файл в порт', command=(lambda: send_file_via_port(None)))
btn_write.pack(side=RIGHT, expand=YES, fill=X)


# define log
lab4 = Label(root, text='Лог процесса')
lab4.pack()
log = Listbox()
log.pack(fill=X)

# define progress bar
pb = Progressbar(root, orient="horizontal", length=40, mode="determinate")
pb['value'] = 0
pb['maximum'] = 100
pb.pack(fill=X)

root.mainloop()
