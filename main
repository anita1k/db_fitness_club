import tkinter
from tkinter import *
from tkinter import messagebox

import clients
import income
import operations
import services

login = Tk()
login.title("Авторизация")
login.geometry('300x300')

def on_closing_l():
    login.destroy()

login.protocol("WM_DELETE_WINDOW", on_closing_l)

def login_command():
    if login_text.get() == "postgres" and password_text.get() == "PASSWORD":
        on_closing_l()
    else:
        log.delete(0, END)
        pas.delete(0, END)
        tkinter.messagebox.showinfo("Ошибка!", "Введен неверный логин или пароль!")


login_text = StringVar()
log = Entry(login, textvariable=login_text)
log.grid(row=2, column=3)

password_text = StringVar()
pas = Entry(login, textvariable=password_text)
pas.grid(row=4, column=3)

l1_log = Label(login, text="Логин")
l1_log.grid(row=1, column=3)

l2_log = Label(login, text="Пароль")
l2_log.grid(row=3, column=3)

b1_log = Button(login, text="Войти", width=12, command=login_command)
b1_log.grid(row=5, column=3)

login.mainloop()

window = Tk()
window.title("Fitness Club")
window.geometry('300x300')


def on_closing():
    if messagebox.askokcancel("", "Закрыть программу?"):
        window.destroy()

window.protocol("WM_DELETE_WINDOW", on_closing)


def clients_table():
    clients.clients_func()


def services_table():
    services.service_func()


def operations_table():
    operations.operations_func()


def income_table():
    income.income_func()

b1 = Button(window, text="Клиенты", width=12, command=clients_table)
b1.grid(row=2, column=3)
b2 = Button(window, text="Услуги", width=12, command=services_table)
b2.grid(row=3, column=3)
b3 = Button(window, text="Операции", width=12, command=operations_table)
b3.grid(row=4, column=3)
b4 = Button(window, text="Доход", width=12, command=income_table)
b4.grid(row=5, column=3)
b5 = Button(window, text="Закрыть", width=12, command=on_closing)
b5.grid(row=7, column=3)

window.mainloop()
