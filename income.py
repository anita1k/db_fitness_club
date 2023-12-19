import tkinter
from tkinter import *
import psycopg2


class Income:
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
            "CREATE OR REPLACE FUNCTION f_create_db(dbname text) RETURNS void AS $func$ BEGIN"
            "IF EXISTS (SELECT 1 FROM pg_database WHERE datname = dbname) THEN RAISE NOTICE 'Database already exists';"
            "ELSE PERFORM dblink_exec('dbname=' || current_database(), 'CREATE DATABASE ' || quote_ident(dbname));"
            "END IF; END $func$ LANGUAGE plpgsql;")
        self.cur.execute(
            "CREATE TABLE IF NOT EXISTS income (incomeid integer NOT NULL UNIQUE PRIMARY KEY,"
            "service varchar(40), sum integer, price integer, FOREIGN KEY (service) REFERENCES services(service),"
            "FOREIGN KEY (service) REFERENCES services(service))")
        self.conn.commit()

    def __del__(self):
        self.conn.close()

    def view(self):
        self.cur.execute("SELECT * FROM income")
        rows = self.cur.fetchall()
        return rows

    def insert(self, service, sum, price):
        self.cur.execute("INSERT INTO income VALUES (DEFAULT,%s,%s,%s)", (service, sum, price,))
        self.conn.commit()

    def update(self, incomeid, service, sum, price):
        self.cur.execute("UPDATE income SET service=%s, sum=%s, price=%s WHERE incomeid=%s",
                         (service, sum, price, incomeid,))
        self.conn.commit()

    def delete(self, incomeid):
        self.cur.execute("DELETE FROM income WHERE incomeid=%s", (incomeid,))
        self.conn.commit()

    def search(self, service=""):
        self.cur.execute("SELECT * FROM income WHERE service=%s", (service,))
        rows = self.cur.fetchall()
        return rows

    def delete_db(self):
        self.cur.execute("DROP DATABASE fitness_club_ [;]")


def income_func():
    inc = Income()
    def get_selected_row():
        global selected_tuple
        index = list1.curselection()[0]
        selected_tuple = list1.get(index)
        e1.delete(0, END)
        e1.insert(END, selected_tuple[1])
        e2.delete(0, END)
        e2.insert(END, selected_tuple[2])
        e3.delete(0, END)
        e3.insert(END, selected_tuple[3])

    def view_command():
        list1.delete(0, END)
        for row in inc.view():
            list1.insert(END, row)

    def search_command():
        list1.delete(0, END)
        for row in inc.search(service_text.get()):
            list1.insert(END, row)

    def add_command():
        inc.insert(service_text.get(), sum_text.get(), price_text.get())
        view_command()

    def delete_command():
        inc.delete(selected_tuple[0])
        view_command()

    def update_command():
        inc.update(selected_tuple[0], service_text.get(), sum_text.get(), price_text.get())
        view_command()

    income_window = tkinter.Toplevel()
    income_window.title("Fitness club - Income")

    l1 = Label(income_window, text="Услуга")
    l1.grid(row=0, column=0)

    l2 = Label(income_window, text="Сумма")
    l2.grid(row=0, column=2)

    l3 = Label(income_window, text="Цена")
    l3.grid(row=1, column=0)

    service_text = StringVar()
    e1 = Entry(income_window, textvariable=service_text)
    e1.grid(row=0, column=1)

    sum_text = StringVar()
    e2 = Entry(income_window, textvariable=sum_text)
    e2.grid(row=0, column=3)

    price_text = StringVar()
    e3 = Entry(income_window, textvariable=price_text)
    e3.grid(row=1, column=1)

    def on_closing():
        income_window.destroy()

    income_window.protocol("WM_DELETE_WINDOW", on_closing)

    list1 = Listbox(income_window, height=25, width=65)
    list1.grid(row=2, column=0, rowspan=6, columnspan=2)

    list1.bind('<<ListboxSelect>>', get_selected_row)

    b1 = Button(income_window, text="Посмотреть все", width=12, command=view_command)
    b1.grid(row=2, column=3)
    b2 = Button(income_window, text="Поиск", width=12, command=search_command)
    b2.grid(row=3, column=3)
    b3 = Button(income_window, text="Добавить", width=12, command=add_command)
    b3.grid(row=4, column=3)
    b4 = Button(income_window, text="Обновить", width=12, command=update_command)
    b4.grid(row=5, column=3)
    b5 = Button(income_window, text="Удалить", width=12, command=delete_command)
    b5.grid(row=6, column=3)
    b6 = Button(income_window, text="Закрыть", width=12, command=on_closing)
    b6.grid(row=7, column=3)

    view_command()
    income_window.mainloop()


if __name__ == '__main__':
    income_func()
    
