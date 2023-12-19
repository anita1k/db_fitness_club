import tkinter
from tkinter import *
import psycopg2


class Operations:
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
            "CREATE TABLE IF NOT EXISTS operations (operation integer NOT NULL UNIQUE PRIMARY KEY,"
            "clientid integer NOT NULL, service varchar(40), FOREIGN KEY (clientid) REFERENCES clients(clientid),"
            "FOREIGN KEY (service) REFERENCES services(service))")
        self.conn.commit()

    def __del__(self):
        self.conn.close()

    def view(self):
        self.cur.execute("SELECT * FROM operations")
        rows = self.cur.fetchall()
        return rows

    def insert(self, clientid, service):
        self.cur.execute("INSERT INTO operations VALUES (DEFAULT,%s,%s)", (clientid, service,))
        self.conn.commit()

    def update(self, operation, clientid, service):
        self.cur.execute("UPDATE operations SET clientid=%s, service=%s WHERE operation=%s",
                         (clientid, service, operation,))
        self.conn.commit()

    def delete(self, operation):
        self.cur.execute("DELETE FROM operations WHERE operation=%s", (operation,))
        self.conn.commit()

    def search(self, clientid=""):
        self.cur.execute("SELECT * FROM operations WHERE clientid=%s", (clientid,))
        rows = self.cur.fetchall()
        return rows


def operations_func():
    op = Operations()
    def get_selected_row():
        global selected_tuple
        index = list1.curselection()[0]
        selected_tuple = list1.get(index)
        e1.delete(0, END)
        e1.insert(END, selected_tuple[1])
        e2.delete(0, END)
        e2.insert(END, selected_tuple[2])

    def view_command():
        list1.delete(0, END)
        for row in op.view():
            list1.insert(END, row)

    def search_command():
        list1.delete(0, END)
        for row in op.search(clientid_text.get()):
            list1.insert(END, row)

    def add_command():
        op.insert(clientid_text.get(), service_text.get())
        view_command()

    def delete_command():
        op.delete(selected_tuple[0])
        view_command()

    def update_command():
        op.update(selected_tuple[0], clientid_text.get(), service_text.get())
        view_command()

    operations_window = tkinter.Toplevel()
    operations_window.title("Fitness club - Operations")

    l1 = Label(operations_window, text="ID клиента")
    l1.grid(row=0, column=0)

    l2 = Label(operations_window, text="Услуга")
    l2.grid(row=0, column=2)

    clientid_text = StringVar()
    e1 = Entry(operations_window, textvariable=clientid_text)
    e1.grid(row=0, column=1)

    service_text = StringVar()
    e2 = Entry(operations_window, textvariable=service_text)
    e2.grid(row=0, column=3)

    def on_closing():
        operations_window.destroy()

    operations_window.protocol("WM_DELETE_WINDOW", on_closing)

    list1 = Listbox(operations_window, height=25, width=65)
    list1.grid(row=2, column=0, rowspan=6, columnspan=2)

    list1.bind('<<ListboxSelect>>', get_selected_row)

    b1 = Button(operations_window, text="Посмотреть все", width=12, command=view_command)
    b1.grid(row=2, column=3)
    b2 = Button(operations_window, text="Поиск", width=12, command=search_command)
    b2.grid(row=3, column=3)
    b3 = Button(operations_window, text="Добавить", width=12, command=add_command)
    b3.grid(row=4, column=3)
    b4 = Button(operations_window, text="Обновить", width=12, command=update_command)
    b4.grid(row=5, column=3)
    b5 = Button(operations_window, text="Удалить", width=12, command=delete_command)
    b5.grid(row=6, column=3)
    b6 = Button(operations_window, text="Закрыть", width=12, command=on_closing)
    b6.grid(row=7, column=3)

    view_command()
    operations_window.mainloop()


if __name__ == '__main__':
    operations_func()
    
