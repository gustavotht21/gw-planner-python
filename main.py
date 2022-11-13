from tkinter import *
from tkinter import messagebox
from connection import *
import sqlite3
import time


def signinScreen(title):

  def login():
    connection = db_connection_start()
    SQL_search_user = "SELECT * FROM usuarios"
    users = db_search_user(connection, SQL_search_user)

    validado = False
    for user in users:
      if user[1] == input_email.get() and user[2] == int(input_password.get()):
        screen.destroy()
        homeScreen("Microsfot - Tarefas")
        validado = True
    if validado == False:
      messagebox.showerror("ERRO", """Erro ao tentar fazer login. Considere:
- Ver se as informações foram escritas corretamente;
- Cadastrar-se caso não possua conta;
- Clicar em "Esqueceu a senha?" para recuperar sua senha, caso a tenha esquecido""")

    db_connection_close(connection)

  screen = Tk()
  screen.title(title)
  screen.geometry('1280x800')

  background = PhotoImage(file='assets/login.png')
  signinButton = PhotoImage(file='assets/signinButton.png')
  signupButton = PhotoImage(file='assets/signupButton.png')

  label = Label(screen, image=background)
  label.pack()

  input_email = Entry(screen, highlightthickness=0, bd=0, font=('Inter', 8), justify=LEFT, foreground='#605672')
  input_email.place(width=370, height=35, x=172, y=353)

  input_password = Entry(screen, highlightthickness=0, bd=0, font=('Inter', 8), justify=LEFT, foreground='#605672')
  input_password.place(width=370, height=35, x=172, y=450)

  button_signin = Button(screen, highlightthickness=0, bd=0, background='#4284F2', image=signinButton, command=login)
  button_signin.place(width=135, height=40, x=171, y=529)

  button_signup = Button( screen, highlightthickness=0, bd=0, background='white', image=signupButton, command=lambda:
  [
      screen.destroy(),
      signupScreen('Microsfot - Cadastro')
  ])
  button_signup.place(width=194, height=45, x=325, y=527)

  screen.mainloop()


def signupScreen(title):

  def verificationEmail():
    emails_extensios = [
      'ifro.edu.br', 'estudante.ifro.edu.br', 'gmail.com', 'hotmail.com',
      'yahoo.com'
    ]

    first_input = input_email.get()
    second_input = input_email_again.get()
    if '@' in first_input.split():
        if first_input.split('@')[1] in emails_extensios:
            if first_input == second_input:
                connection = db_connection_start()
                SQL_create_table = """
                CREATE TABLE IF NOT EXISTS usuarios (
                  id integer PRMARY KEY IDENTITY(1, 1),
                  email text NOT NULL,
                  senha integer NOT NULL
                ); """
                db_table_create(connection, SQL_create_table)

                SQL_insert_user = (
                  f'INSERT INTO usuarios (email, senha) VALUES ("{first_input}",{input_password.get()})'
                )
                db_user_insert(connection, SQL_insert_user)

                db_connection_close(connection)

                time.sleep(0.5)
                screen.destroy(),
                signinScreen('Microsfot - Login')
            else:
                messagebox.showerror("ERRO", """Os emails devem ser iguais""")
        else:
            messagebox.showerror("ERRO", """Insira um email válido""")
    else:
        messagebox.showerror("ERRO", """Insira um email válido""")

  screen = Tk()
  screen.title(title)
  screen.geometry('1280x800')

  background = PhotoImage(file='assets/signup.png')
  finalizeButton = PhotoImage(file='assets/finalizeButton.png')
  backButton = PhotoImage(file='assets/BackButton.png')

  label = Label(screen, image=background)
  label.pack()

  input_email = Entry(screen, highlightthickness=0, bd=0, font=('Inter', 8), justify=LEFT, foreground='#605672')
  input_email.place(width=370, height=35, x=172, y=328)

  input_email_again = Entry(screen, highlightthickness=0, bd=0, font=('Inter', 8), justify=LEFT, foreground='#605672')
  input_email_again.place(width=370, height=35, x=172, y=393)

  input_password = Entry(screen, highlightthickness=0, bd=0, font=('Inter', 8), justify=LEFT, foreground='#605672')
  input_password.place(width=370, height=35, x=172, y=458)

  button_signin = Button(screen, highlightthickness=0, bd=0, background='#4284F2', image=finalizeButton, command=verificationEmail)
  button_signin.place(width=225, height=40, x=172, y=538)

  button_back = Button(screen, highlightthickness=0, bd=0, background='white', image=backButton, command=lambda:
  [
      screen.destroy(),
      signinScreen('Microsfot - Tela Inicial')
  ])
  button_back.place(width=131, height=45, x=415, y=537)


  screen.mainloop()


def homeScreen(title):
  screen = Tk()
  screen.title(title)
  screen.geometry('1280x800')

  background = PhotoImage(file='assets/homeplanner.png')
  editButton = PhotoImage(file='assets/editButton.png')
  signoutButton = PhotoImage(file='assets/signOutButton.png')

  label = Label(screen, image=background)
  label.pack()

  button_edit = Button(screen, highlightthickness=0, bd=0, background='#4284F2', image=editButton, command=lambda:
    [screen.destroy(),
     editScreen('Microsfot - Editar Tarefas')])
  button_edit.place(width=36.5, height=36.5, x=91, y=122)

  button_signout = Button(screen, highlightthickness=0, bd=1, background='#749FE4', image=signoutButton, command=lambda:
  [
      screen.destroy(),
      signinScreen('Microsfot - Tela Inicial')
  ])
  button_signout.place(width=112, height=45, x=1090, y=722)


  button_signout = Button(screen, highlightthickness=0, bd=1, background='#749FE4', image=signoutButton, command=lambda: [
      screen.destroy(),
      signinScreen('Microsfot - Tela Inicial')
    ]
  )
  button_signout.place(width=112, height=45, x=1090, y=722)

  # connection = db_connection_start()
  # for event in events:
  #   print(f'{event[1]} | {event[2]}')
  # db_connection_close(connection)

  screen.mainloop()


def editScreen(title):

  def saveDatas():
    connection = db_connection_start()
    SQL_table_clear = """
          DELETE FROM eventos;
            """
    db_table_clear(connection, SQL_table_clear)

    SQL_create_table = """   
          CREATE TABLE IF NOT EXISTS eventos (                  
            id integer PRIMARY KEY AUTOINCREMENT,
            titulo text NOT NULL,
            diaSemana text NOT NULL
          ); """
    db_table_create(connection, SQL_create_table)

    for index in range(12):
      print(sunday[index].get())
      # SQL_insert_user = (
      #   f'INSERT INTO eventos (titulo, diaSemana) VALUES ("{valoresSunday[row]}", "sunday")'
      # )
      # db_user_insert(connection, SQL_insert_user)

      # SQL_insert_user = (
      #   f'INSERT INTO eventos (titulo, diaSemana) VALUES ("{str(monday[row])}", "monday")'
      # )
      # db_user_insert(connection, SQL_insert_user)

      # SQL_insert_user = (
      #   f'INSERT INTO eventos (titulo, diaSemana) VALUES ("{tuesday[row]}", "tuesday")'
      # )
      # db_user_insert(connection, SQL_insert_user)

      # SQL_insert_user = (
      #   f'INSERT INTO eventos (titulo, diaSemana) VALUES ("{wednesday[row]}", "wednesday")'
      # )
      # db_user_insert(connection, SQL_insert_user)

      # SQL_insert_user = (
      #   f'INSERT INTO eventos (titulo, diaSemana) VALUES ("{thursday[row]}", "thursday")'
      # )
      # db_user_insert(connection, SQL_insert_user)

      # SQL_insert_user = (
      #   f'INSERT INTO eventos (titulo, diaSemana) VALUES ("{friday[row]}", "friday")'
      # )
      # db_user_insert(connection, SQL_insert_user)

      # SQL_insert_user = (
      #   f'INSERT INTO eventos (titulo, diaSemana) VALUES ("{saturday[row]}", "saturday")'
      # )
      # db_user_insert(connection, SQL_insert_user)

    SQL_search_events = "SELECT * FROM eventos"
    events = db_search_events(connection, SQL_search_events)

    db_connection_close(connection)

  screen = Tk()
  screen.title(title)
  screen.geometry('1280x800')

  background = PhotoImage(file='assets/edit.png')
  confirmButton = PhotoImage(file='assets/confirmButton.png')

  label = Label(screen, image=background)
  label.pack()

  button_confirm = Button(screen, highlightthickness=0, bd=0, background='#4284F2', image=confirmButton, command=lambda:
    [saveDatas(),
     screen.destroy(),
     homeScreen('Microsfot - Tarefas')])
  button_confirm.place(width=36.5, height=36.5, x=91, y=122)

  # sunday =   ['---', '---', '---', '---', '---', '---', '---', '---', '---', '---', '---', '---']
  sunday = [
    'sunday1', 'sunday2', 'sunday3', 'sunday4', 'sunday5'
    'sunday6', 'sunday7', 'sunday8', 'sunday9', 'sunday10', 'sunday11',
    'sunday12', 'sunday13', 'sunday14'
  ]
  # monday =   ['---', '---', '---', '---', '---', '---', '---', '---', '---', '---', '---', '---']
  # tuesday =  ['---', '---', '---', '---', '---', '---', '---', '---', '---', '---', '---', '---']
  # wednesday =['---', '---', '---', '---', '---', '---', '---', '---', '---', '---', '---', '---']
  # thursday = ['---', '---', '---', '---', '---', '---', '---', '---', '---', '---', '---', '---']
  # friday =   ['---', '---', '---', '---', '---', '---', '---', '---', '---', '---', '---', '---']
  # saturday = ['---', '---', '---', '---', '---', '---', '---', '---', '---', '---', '---', '---']
  y = 233
  for index in range(12):
    sunday[index] = Entry(screen, highlightthickness=0, bd=2, font=('Inter', 8), justify=LEFT, foreground='#605672')
    sunday[index].place(width=98, height=23, x=153, y=y)
    y += 40

  # indexDays = 0
  # for y in range(233, 608, 33):
  #   monday[indexDays] = Entry(screen, highlightthickness=0, bd=0, font=('Inter', 8), justify=LEFT, foreground='#605672')
  #   monday[indexDays].place(width=98, height=23, x=299, y=y)
  #   indexDays += 1

  # indexDays = 0
  # for y in range(233, 608, 33):
  #   tuesday[indexDays] = Entry(screen, highlightthickness=0, bd=0, font=('Inter', 8), justify=LEFT, foreground='#605672')
  #   tuesday[indexDays].place(width=98, height=23, x=445, y=y)
  #   indexDays += 1

  # indexDays = 0
  # for y in range(233, 608, 33):
  #   wednesday[indexDays] = Entry(screen, highlightthickness=0, bd=0, font=('Inter', 8), justify=LEFT, foreground='#605672')
  #   wednesday[indexDays].place(width=98, height=23, x=591, y=y)
  #   indexDays += 1

  # indexDays = 0
  # for y in range(233, 608, 33):
  #   thursday[indexDays] = Entry(screen, highlightthickness=0, bd=0, font=('Inter', 8), justify=LEFT, foreground='#605672')
  #   thursday[indexDays].place(width=98, height=23, x=737, y=y)
  #   indexDays += 1

  # indexDays = 0
  # for y in range(233, 608, 33):
  #   friday[indexDays] = Entry(screen, highlightthickness=0, bd=0, font=('Inter', 8), justify=LEFT, foreground='#605672')
  #   friday[indexDays].place(width=98, height=23, x=883, y=y)
  #   indexDays += 1

  # indexDays = 0
  # for y in range(233, 608, 33):
  #   saturday[indexDays] = Entry(screen, highlightthickness=0, bd=0, font=('Inter', 8), justify=LEFT, foreground='#605672')
  #   saturday[indexDays].place(width=98, height=23, x=1029, y=y)
  #   indexDays += 1
  screen.mainloop()


signinScreen('Microsfot - Tela Inicial')
