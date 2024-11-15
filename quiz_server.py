import socket
from threading import Thread
import random

server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

ip = '127.0.0.1'
port = 8000
server.bind((ip,port))
server.listen()
print("Server is running...")

clients = []
nicknames = []
questions = [
"What is the longest word in the English language? \n A: Antidisestablishmentarianism \n B: Hippopotomonstrosesquippedaliophobia \n C: Floccinaucinihilipilification",
"What is the name of the worlds smallest horse?  \n A: Falabella \n B: Shetland pony \n C: Miniature horse",
"What is Benedictine monk Dom Pierre Pérignon rumored to have created? \n A: Tomato ketchup \n B: Champagne \n C: French fries",
"Which country drinks the most amount of coffee per person? \n A: Finland \n B: Italy \n C: Colombia ",
"What is the collective name for a group of unicorns? \n A: A sparkle \n B: A spell \n C: A blessing",
"What is the most common color of toilet paper in France? \n A: Pink \n B: White \n C: Blue",
"How many years old is the worlds oldest piece of chewing gum? \n A: 100 \n Bf: 2,500 \n C: 5,700",
"How many times per day does the average American open their fridge? \n A: 5 \n B: 22 \n C: 33",
"What color is an airplanes famous black box? \n A: Red \n B: Orange \n C: Black",
"What is Bombay Ducks main ingredient? \n A: Fish \n B: Duck \n C: Chicken"]
answers = [
    'a','c','b','a','c','a','c','c','b','a'
]

def clientThread(conn,addr,nickname):
    score = 0
    conn.send("Welcome to the game!\n".encode("utf-8"))
    conn.send("You will recieve a question, find the right answer to it!\n".encode("utf-8"))
    conn.send("Good luck!\n\n".encode("utf-8"))

    index, question, answer = get_random_question_answer(conn,addr)

    while True:
        try:
            message = conn.recv(2048).decode("utf-8")
            if message=="ANSWER":
                if message.lower == answer:
                    score +=1
                    conn.send("Your answer was correct!".encode("utf-8"))
                    conn.send(f"Your score is now{score}".encode("utf-8"))
                else:
                    conn.send("Your answer was incorrect, better luck next time".encode("utf-8"))
                    conn.send(f"Your score is {score}".encode("utf-8"))
                remove_question(index)
                index, question, answer = get_random_question_answer(conn,addr)
        except:
            broadcast(conn,nickname)
        
def remove_question(index):
    questions.pop(index)
    answers.pop(index)

def broadcast(conn,nickname):
    for client in clients:
        if client==conn:
            remove_client(conn)
            remove_nickname(nickname)

def remove_client(conn):
    if conn in clients:
        clients.remove(conn)

def remove_nickname(nickname):
    if nickname in nicknames:
        nicknames.remove(nickname)

def get_random_question_answer(conn,addr):
    random_question = random.randint(0,len(questions)-1)
    question = questions[random_question]
    answer = answers[random_question]
    conn.send(question.encode("utf-8"))

    return random_question,question,answer

while True:
    conn,addr = server.accept()

    clients.append(conn)
    print(addr[0]+"connected")

    conn.send("NICKNAME".encode("utf-8"))
    nickname = conn.recv(2048).decode("utf-8")
    nicknames.append(nickname)
    message = '{} joined'.format(nickname)
    print(message)

    new_thread = Thread(target=clientThread,args=(conn,addr,nickname))
    new_thread.start()