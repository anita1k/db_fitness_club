import tkinter
from tkinter import *
import psycopg2

class Clients:
    def __init__(self):
        self.conn = psycopg2.connect(
            database="fitness_club",
            user="postgres",
            password="PASSWORD",
            host="127.0.0.1",
            port="5432"
        )
        self.cur = self.conn.cursor()
        self.cur.execute(
            "CREATE TABLE IF NOT EXISTS clients (clientid integer NOT NULL PRIMARY KEY,"
            "surname varchar(30) NOT NULL,name varchar(30) NOT NULL,patronymic varchar(30),"
            "age integer NOT NULL,CHECK(age <= 100 AND age >= 0))")
        self.conn.commit()

    def __del__(self):
        self.conn.close()

    def view(self):
        self.cur.execute("SELECT * FROM clients")
        rows = self.cur.fetchall()
        return rows

    def insert(self, surname, name, patronymic, age):
        self.cur.execute("INSERT INTO clients VALUES (DEFAULT,%s,%s,%s,%s)", (surname, name, patronymic, age,))
        self.conn.commit()

    def update(self, clientid, surname, name, patronymic, age):
        self.cur.execute("UPDATE clients SET surname=%s, name=%s, patronymic=%s, age=%s WHERE clientid=%s",
                         (surname, name, patronymic, age, clientid,))
        self.conn.commit()

    def delete(self, clientid):
        self.cur.execute("DELETE FROM clients WHERE clientid=%s", (clientid,))
        self.conn.commit()

    def search(self, surname=""):
        self.cur.execute("SELECT * FROM clients WHERE surname=%s", (surname,))
        rows = self.cur.fetchall()
        return rows




def clients_func():
    cl = Clients()
    def get_selected_row(event):
        global selected_tuple
        index = list1.curselection()[0]
        selected_tuple = list1.get(index)
        e1.delete(0, END)
        e1.insert(END, selected_tuple[1])
        e2.delete(0, END)
        e2.insert(END, selected_tuple[2])
        e3.delete(0, END)
        e3.insert(END, selected_tuple[3])
        e4.delete(0, END)
        e4.insert(END, selected_tuple[4])

    def view_command():
        list1.delete(0, END)
        for row in cl.view():
            list1.insert(END, row)

    def search_command():
        list1.delete(0, END)
        for row in cl.search(surname_text.get()):
            list1.insert(END, row)

    def add_command():
        cl.insert(surname_text.get(), name_text.get(), patronymic_text.get(), age_text.get())
        view_command()

    def delete_command():
        cl.delete(selected_tuple[0])
        view_command()

    def update_command():
        cl.update(selected_tuple[0], surname_text.get(), name_text.get(), patronymic_text.get(), age_text.get())
        view_command()

    clients_window = tkinter.Toplevel()
    clients_window.title("Fitness club - Clients")

    l1 = Label(clients_window, text="Фамилия")
    l1.grid(row=0, column=0)

    l2 = Label(clients_window, text="Имя")
    l2.grid(row=0, column=2)

    l3 = Label(clients_window, text="Отчество")
    l3.grid(row=1, column=0)

    l4 = Label(clients_window, text="Возраст")
    l4.grid(row=1, column=2)

    surname_text = StringVar()
    e1 = Entry(clients_window, textvariable=surname_text)
    e1.grid(row=0, column=1)

    name_text = StringVar()
    e2 = Entry(clients_window, textvariable=name_text)
    e2.grid(row=0, column=3)

    patronymic_text = StringVar()
    e3 = Entry(clients_window, textvariable=patronymic_text)
    e3.grid(row=1, column=1)

    age_text = StringVar()
    e4 = Entry(clients_window, textvariable=age_text)
    e4.grid(row=1, column=3)

    def on_closing():
        clients_window.destroy()

    clients_window.protocol("WM_DELETE_WINDOW", on_closing)

    list1 = Listbox(clients_window, height=25, width=65)
    list1.grid(row=2, column=0, rowspan=6, columnspan=2)

    list1.bind('<<ListboxSelect>>', get_selected_row)

    b1 = Button(clients_window, text="Посмотреть все", width=12, command=view_command)
    b1.grid(row=2, column=3)
    b2 = Button(clients_window, text="Поиск", width=12, command=search_command)
    b2.grid(row=3, column=3)
    b3 = Button(clients_window, text="Добавить", width=12, command=add_command)
    b3.grid(row=4, column=3)
    b4 = Button(clients_window, text="Обновить", width=12, command=update_command)
    b4.grid(row=5, column=3)
    b5 = Button(clients_window, text="Удалить", width=12, command=delete_command)
    b5.grid(row=6, column=3)
    b6 = Button(clients_window, text="Закрыть", width=12, command=on_closing)
    b6.grid(row=7, column=3)

    view_command()
    clients_window.mainloop()


if __name__ == '__main__':
    clients_func()
    
