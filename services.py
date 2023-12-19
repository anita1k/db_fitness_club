import tkinter
from tkinter import *
import psycopg2


class Services:
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
            "CREATE TABLE IF NOT EXISTS services (service varchar(40) UNIQUE NOT NULL PRIMARY KEY, price integer)")
        self.conn.commit()

    def __del__(self):
        self.conn.close()

    def view(self):
        self.cur.execute("SELECT * FROM services")
        rows = self.cur.fetchall()
        return rows

    def insert(self, service, price):
        self.cur.execute("INSERT INTO services VALUES (%s,%s)", (service, price,))
        self.conn.commit()

    def update(self, service, price):
        self.cur.execute("UPDATE services SET price=%s WHERE service=%s",
                         (price, service,))
        self.conn.commit()

    def delete(self, service):
        self.cur.execute("DELETE FROM services WHERE service=%s", (service,))
        self.conn.commit()

    def search(self, service=""):
        self.cur.execute("SELECT * FROM services WHERE service=%s", (service,))
        rows = self.cur.fetchall()
        return rows


def service_func():
    sv = Services()

    def get_selected_row(event):
        global selected_tuple
        index = list1.curselection()[0]
        selected_tuple = list1.get(index)
        e1.delete(0, END)
        e1.insert(END, selected_tuple[0])
        e2.delete(0, END)
        e2.insert(END, selected_tuple[1])

    def view_command():
        list1.delete(0, END)
        for row in sv.view():
            list1.insert(END, row)

    def search_command():
        list1.delete(0, END)
        for row in sv.search(service_text.get()):
            list1.insert(END, row)

    def add_command():
        sv.insert(service_text.get(), price_text.get())
        view_command()

    def delete_command():
        sv.delete(selected_tuple[0])
        view_command()

    def update_command():
        sv.update(selected_tuple[0], price_text.get())
        view_command()

    service_window = tkinter.Toplevel()
    service_window.title("Fitness club - Services")

    l1 = Label(service_window, text="Название услуги")
    l1.grid(row=0, column=0)

    l2 = Label(service_window, text="Цена")
    l2.grid(row=0, column=2)

    service_text = StringVar()
    e1 = Entry(service_window, textvariable=service_text)
    e1.grid(row=0, column=1)

    price_text = StringVar()
    e2 = Entry(service_window, textvariable=price_text)
    e2.grid(row=0, column=3)

    def on_closing():
        service_window.destroy()

    service_window.protocol("WM_DELETE_WINDOW", on_closing)

    list1 = Listbox(service_window, height=25, width=65)
    list1.grid(row=2, column=0, rowspan=6, columnspan=2)

    list1.bind('<<ListboxSelect>>', get_selected_row)

    b1 = Button(service_window, text="Посмотреть все", width=12, command=view_command)
    b1.grid(row=2, column=3)
    b2 = Button(service_window, text="Поиск", width=12, command=search_command)
    b2.grid(row=3, column=3)
    b3 = Button(service_window, text="Добавить", width=12, command=add_command)
    b3.grid(row=4, column=3)
    b4 = Button(service_window, text="Обновить", width=12, command=update_command)
    b4.grid(row=5, column=3)
    b5 = Button(service_window, text="Удалить", width=12, command=delete_command)
    b5.grid(row=6, column=3)
    b6 = Button(service_window, text="Закрыть", width=12, command=on_closing)
    b6.grid(row=7, column=3)

    view_command()
    service_window.mainloop()


if __name__ == '__main__':
    service_func()
