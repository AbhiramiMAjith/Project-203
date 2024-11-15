import socket
from threading import Thread
from tkinter import *

#nickname = input("Enter your nickname ")

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

ip = '127.0.0.1'
port = 8000
client.connect((ip,port))

class GUI:
    def __init__(self):
        self.window = Tk()
        self.window.withdraw()

        self.login = Toplevel()
        self.login.title("Login")

        self.login.resizable(width=False,height=False)
        self.login.configure(width=400,height=300)

        self.ask = Label(self.login,text="Please Login to continue",justify='center',font=('Calibri'))
        self.ask.place(relheight = 0.15,relx = 0.2,rely = 0.07)

        self.name_label = Label(self.login,text="Name",font=("Calibri"))
        self.name_label.place(relheight = 0.2,relx = 0.1,rely = 0.2)

        self.name = Entry(self.login)
        self.name.place(relwidth = 0.4,relheight = 0.12, relx= 0.1,rely = 0.2)

        self.continue_button = Button(self.login,text="Continue",font=("Calibri"),command=lambda:self.go_ahead(self.name.get()))
        self.continue_button.place(relx=0.4,rely=0.55)

        self.window.mainloop()

    def go_ahead(self,name):
        self.login.destroy()
        recieve_thread = Thread(target=self.recieve)
        recieve_thread.start()

        self.layout(name)

    def recieve(self):
        while True:
            try:
                message = client.recv(2048).decode("utf-8")
                if message == 'NICKNAME':
                    client.send(self.name.encode("utf-8"))
                else:
                    self.show_message(message)
            except Exception as error:
                print("An error occured",error)
                client.close()
                break

    def layout(self,name):
        self.name = name
        self.window.deiconify()
        self.window.title("Chat app")
        self.window.resizable(height=False,width=False)
        self.window.config(width=470,height=550,bg="#17202a")

        self.name_label = Label(self.window,text=self.name,fg="black",bg="lightyellow",font="Calibri")
        self.name_label.place(relwidth=1)

        self.line = Label(self.window,fg="white")
        self.line.place(relwidth=1,relheight=0.001,rely=0.05)

        self.textCon = Text(self.window)
        self.textCon.place(relwidth=0.9,relheight=0.6,rely=0.1,relx=0.05)

        self.entry_message = Entry(self.window,bg="lightyellow")
        self.entry_message.place(relwidth=0.7,relheight=0.1,rely=0.8)
        self.entry_message.focus()

        self.button = Button(self.window,text='Send',bg="white",fg="black",font="Calibri",command=lambda:self.send_message(self.entry_message.get()))
        self.button.place(relwidth=0.2,relheight=0.1,rely=0.8,relx=0.8)

    def send_message(self,message):
        self.textCon.config(state=DISABLED)
        self.msg = message
        self.entry_message.delete(0,END)
        display = Thread(target=self.write)
        display.start()

    def show_message(self,message):
        self.textCon.config(state=NORMAL)
        self.textCon.insert(END,message+"\n\n")
        self.textCon.config(state=DISABLED)
        self.textCon.see(END)

    def write(self):
        self.textCon.config(state=DISABLED)

        while True:
            message = (f"{self.name}:{self.msg}")
            print(message)
            #client.send(message.encode("utf-8"))
            self.show_message(message)
            break

gui = GUI()