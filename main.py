import tkinter as tk
import db


class EntryWithPlaceholder(tk.Entry):
    def __init__(self, master=None, placeholder="PLACEHOLDER", color='grey'):
        super().__init__(master)

        self.placeholder = placeholder
        self.placeholder_color = color
        self.default_fg_color = self['fg']

        self.bind("<FocusIn>", self.foc_in)
        self.bind("<FocusOut>", self.foc_out)

        self.put_placeholder()

    def put_placeholder(self):
        self.insert(0, self.placeholder)
        self['fg'] = self.placeholder_color

    def foc_in(self, *args):
        if self['fg'] == self.placeholder_color:
            self.delete('0', 'end')
            self['fg'] = self.default_fg_color

    def foc_out(self, *args):
        if not self.get():
            self.put_placeholder()


class Window(tk.Frame):
    def __init__(self, master=None):
        tk.Frame.__init__(self, master)
        self.master = master
        self.pack(fill=tk.BOTH, expand=1)

        self.main_B1 = tk.Button(self, text='Вывести все обьекты', width=35, command=self.show_all)
        self.main_B2 = tk.Button(self, text='Добавить новый обьект', width=35, command=self.main_to_add)
        self.main_B3 = tk.Button(self, text='Поиск', width=35, command=self.main_to_find)
        self.main_B4 = tk.Button(self, text='Выход', width=35,command=quit)

        self.find_B1 = tk.Button(self, text='Поиск по модели', width=35, command=lambda: self.to_find_str('model'))
        self.find_B2 = tk.Button(self, text='Поиск по бренду', width=35, command=lambda: self.to_find_str('label'))
        self.find_B3 = tk.Button(self, text='Поиск по диагонали', width=35,
                                 command=lambda: self.to_find_int('diagonal'))
        self.find_B4 = tk.Button(self, text='Поиск по частоте', width=35, command=lambda: self.to_find_int('frequency'))
        self.find_B5 = tk.Button(self, text='Поиск по цене', width=35, command=lambda: self.to_find_int('cost'))

        self.find_type = ''

        self.find_int_b1 = tk.Button(self, text=">", width=35, command=lambda: self.find_int('>'))
        self.find_int_b2 = tk.Button(self, text="<", width=35, command=lambda: self.find_int('<'))
        self.find_int_b3 = tk.Button(self, text="=", width=35, command=lambda: self.find_int('=='))
        self.find_int_b4 = tk.Button(self, text="На главную", width=35, command=self.find_int_to_main)

        self.find_str_B1 = tk.Button(self, width=35, text='поиск', command=self.find_str)
        self.find_str_B2 = tk.Button(self,width=35,text='На главную', command=self.find_str_to_main)

        self.Entry = tk.Entry(self, width=35)

        self.add_b1 = tk.Button(self, text="Добавить", width=35, command=self.add)
        self.add_b2 = tk.Button(self, text="На главную", width=35, command=self.add_to_main)
        self.add_E1 = EntryWithPlaceholder(self, 'Бренд')
        self.add_E2 = EntryWithPlaceholder(self, 'Модель')
        self.add_E3 = EntryWithPlaceholder(self, 'Диагональ')
        self.add_E4 = EntryWithPlaceholder(self, 'Частота')
        self.add_E5 = EntryWithPlaceholder(self, 'Стоимость')

        self.T = tk.Text(self, width=80, height=13, bg="black", fg='white', wrap=tk.WORD)
        self.T.place(x=300, y=0)

        self.place_main()


    def find_str_to_main(self):
        self.forget_str_find()
        self.place_main()

    def find_int_to_main(self):
        self.forget_int_find()
        self.place_main()

    def find_str(self):
        type = self.find_type
        value = self.Entry.get()
        self.T.insert(tk.END, '|' + '-' * 56 + '|\n')
        for mon in db.find_str(type=type, value=value):
            self.T.insert(tk.END, '| {:10s} {:10s} {:10s} {:10s} {:10s} |\n'.format(mon.label, str(mon.cost), mon.model,
                                                                                    str(mon.diagonal),
                                                                                    str(mon.frequency)))
        self.T.insert(tk.END, '|' + '-' * 56 + '|\n')

    def find_int(self, sign):
        type = self.find_type
        value = self.Entry.get()
        self.T.insert(tk.END, '|' + '-' * 56 + '|\n')
        for mon in db.find_int(type=type, sign=sign, value=value):
            self.T.insert(tk.END, '| {:10s} {:10s} {:10s} {:10s} {:10s} |\n'.format(mon.label, str(mon.cost), mon.model,
                                                                                    str(mon.diagonal),
                                                                                    str(mon.frequency)))
        self.T.insert(tk.END, '|' + '-' * 56 + '|\n')

    def show_all(self):
        self.T.insert(tk.END, '|' + '-' * 56 + '|\n')
        for mon in db.get_all():
            self.T.insert(tk.END, '| {:10s} {:10s} {:10s} {:10s} {:10s} |\n'.format(mon.label, str(mon.cost), mon.model,
                                                                                    str(mon.diagonal),
                                                                                    str(mon.frequency)))
        self.T.insert(tk.END, '|' + '-' * 56 + '|\n')

    def main_to_add(self):
        self.forget_main()
        self.place_add()

    def add_to_main(self):
        self.forget_add()
        self.place_main()

    def add(self):
        label = self.add_E1.get()
        model = self.add_E2.get()
        diagonal = self.add_E3.get()
        frequency = self.add_E4.get()
        cost = self.add_E5.get()
        db.create(label=label, model=model, diagonal=diagonal, frequency=frequency, cost=cost)

    def place_add(self):
        self.add_E1.place(x=0, y=0)
        self.add_E2.place(x=0, y=30)
        self.add_E3.place(x=0, y=60)
        self.add_E4.place(x=0, y=90)
        self.add_E5.place(x=0, y=120)
        self.add_b1.place(x=0, y=150)
        self.add_b2.place(x=0, y=180)

    def forget_add(self):
        self.add_E1.place_forget()
        self.add_E2.place_forget()
        self.add_E3.place_forget()
        self.add_E4.place_forget()
        self.add_E5.place_forget()
        self.add_b1.place_forget()
        self.add_b2.place_forget()

    def to_find_str(self, type):
        self.forget_find()
        self.place_str_find()
        self.find_type = type

    def to_find_int(self, type):
        self.forget_find()
        self.place_int_find()
        self.find_type = type

    def place_int_find(self):
        self.find_int_b1.place(x=0, y=0)
        self.find_int_b2.place(x=0, y=30)
        self.find_int_b3.place(x=0, y=60)
        self.Entry.place(x=0, y=90)
        self.find_int_b4.place(x=0,y=120)

    def forget_int_find(self):
        self.find_int_b1.place_forget()
        self.find_int_b2.place_forget()
        self.find_int_b3.place_forget()
        self.Entry.place_forget()
        self.find_int_b4.place_forget()

    def place_str_find(self):
        self.find_str_B1.place(x=0, y=0)
        self.Entry.place(x=0, y=30)
        self.find_str_B2.place(x=0,y=60)

    def forget_str_find(self):
        self.find_str_B1.place_forget()
        self.Entry.place_forget()
        self.find_str_B2.place_forget()

    def place_main(self):
        self.main_B1.place(x=0, y=0)
        self.main_B2.place(x=0, y=30)
        self.main_B3.place(x=0, y=60)
        self.main_B4.place(x=0, y=90)

    def forget_main(self):
        self.main_B1.place_forget()
        self.main_B2.place_forget()
        self.main_B3.place_forget()
        self.main_B4.place_forget()

    def place_find(self):
        self.find_B1.place(x=0, y=0)
        self.find_B2.place(x=0, y=30)
        self.find_B3.place(x=0, y=60)
        self.find_B4.place(x=0, y=90)
        self.find_B5.place(x=0, y=120)

    def forget_find(self):
        self.find_B1.place_forget()
        self.find_B2.place_forget()
        self.find_B3.place_forget()
        self.find_B4.place_forget()
        self.find_B5.place_forget()

    def main_to_find(self):
        self.forget_main()
        self.place_find()


if __name__ == '__main__':
    root = tk.Tk()
    app = Window(root)
    root.geometry("950x500")
    root.mainloop()
