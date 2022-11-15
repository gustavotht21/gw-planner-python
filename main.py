import random
from tkinter import *
from tkinter import messagebox

import time
import smtplib
import sqlite3
import email.message
from connection import *
from classes import Usuario

global userObjects
userObjects = []

def signinScreen(title):

  def login():
    connection = db_connection_start()
    SQL_search_user = "SELECT * FROM usuarios"
    users = db_search_user(connection, SQL_search_user)
    validado = False
    for user in users:
      if user[1] == input_email.get() and user[2] == input_password.get():
        if not userObjects or len(userObjects) < len(users):
          nameNewObjectUser = f'User{user[0]}'
          nameNewObjectUser = Usuario(user[0], user[1], user[2])
          userObjects.append(nameNewObjectUser)
        validado = True
        userObjects[user[0]-1].getUserInformations()
        userObjects[user[0]-1].realizarLogin(user[1], user[2])
        screen.destroy()
        homeScreen("Microsfot - Tarefas")
    if validado == False:
      messagebox.showerror("ERRO", """Erro ao tentar fazer login. Considere:
- Ver se as informações foram escritas corretamente;
- Cadastrar-se caso não possua conta;
- Clicar em "Esqueceu a senha?" para recuperar sua senha, caso a tenha esquecido""")
      input_email.delete(0, END)
      input_password.delete(0, END)

    db_connection_close(connection)





  screen = Tk()
  screen.title(title)
  screen.geometry('1280x800')

  background = PhotoImage(file='assets/backgrounds/login.png')
  signinButton = PhotoImage(file='assets/components/signinButton.png')
  signupButton = PhotoImage(file='assets/components/signupButton.png')
  forgetButton = PhotoImage(file='assets/components/ButtonForgetPassword.png')


  label = Label(screen, image=background)
  label.pack()

  input_email = Entry(screen, highlightthickness=0, bd=0, font=('Inter', 8), justify=LEFT, foreground='#605672')
  input_email.place(width=370, height=35, x=172, y=353)

  input_password = Entry(screen, highlightthickness=0, bd=0, font=('Inter', 8), justify=LEFT, foreground='#605672')
  input_password.place(width=370, height=35, x=172, y=450)

  button_signin = Button(screen, highlightthickness=0, bd=0, background='#4284F2', image=signinButton, command=login)
  button_signin.place(width=135, height=40, x=171, y=529)

  button_signup = Button(screen, highlightthickness=0, bd=0, background='white', image=signupButton, command=lambda:
  [
      screen.destroy(),
      signupScreen('Microsfot - Cadastro')
  ])
  button_signup.place(width=194, height=45, x=325, y=527)

  button_forget = Button(screen, highlightthickness=0, bd=0, background='white', image=forgetButton, command=lambda:
  [
    screen.destroy(),
    editPassword("Microsfot - Redefinir senha")
  ])
  button_forget.place(width=146, height=17, x=401, y=495)


  screen.mainloop()


def signupScreen(title):

  def verificationEmail():
    emails_extensios = [
      'ifro.edu.br', 'estudante.ifro.edu.br', 'gmail.com', 'hotmail.com',
      'yahoo.com'
    ]
    simbols = [
      '@', '#', '$', '%', '&',
    ]

    first_input = input_email.get()
    second_input = input_email_again.get()
    password = input_password.get()
    senhaForte = False

    if '@' in list(first_input):
      if first_input.split('@')[1] in emails_extensios:
        if first_input == second_input:
          if len(password) >= 8:
            if password.upper() != password and password.lower() != password:
              for simbol in simbols:
                if simbol in list(password):
                  senhaForte = True
                  connection = db_connection_start()
                  SQL_create_table = """
                  CREATE TABLE IF NOT EXISTS usuarios (                  
                  idUser integer PRIMARY KEY AUTOINCREMENT,
                  email text NOT NULL,
                  senha text NOT NULL
                  ); """
                  db_table_create(connection, SQL_create_table)

                  SQL_insert_user = (
                    f'INSERT INTO usuarios (email, senha) VALUES ("{first_input}","{password}")'
                  )
                  db_user_insert(connection, SQL_insert_user)

                  SQL_search_user = """SELECT idUser FROM usuarios
                  ORDER BY idUser DESC
                  LIMIT 1;"""
                  user = db_search_user(connection, SQL_search_user)

                  lastUserId = user[0]
                  if lastUserId == None:
                    lastUserId = 0
                  nameNewObjectUser = f'User{lastUserId}'
                  nameNewObjectUser = Usuario(lastUserId, first_input, password)

                  userObjects.append(nameNewObjectUser)

                  db_connection_close(connection)

                  messagebox.showinfo("SUCESSO", """Conta criada com sucesso""")

                  time.sleep(0.5)
                  screen.destroy(),
                  signinScreen('Microsfot - Login')
              if senhaForte != True:
                messagebox.showerror("ERRO", """Senha muito fraca: Insira algum símbolo especial
                (Ex: @, #, % etc.)""")
            else:
              messagebox.showerror("ERRO", """Senha muito fraca: Insira letras maiúsculas e minúsculas""")
          else:
            messagebox.showerror("ERRO", """Senha muito fraca: Senha muito pequena""")
        else:
          messagebox.showerror("ERRO", """Os emails devem ser iguais""")
      else:
        messagebox.showerror("ERRO", """Insira um email válido.""")
        input_email.delete(0, END)
        input_email_again.delete(0, END)
    else:
      messagebox.showerror("ERRO", """Insira um email válido.""")
      input_email.delete(0, END)
      input_email_again.delete(0, END)
  screen = Tk()
  screen.title(title)
  screen.geometry('1280x800')

  background = PhotoImage(file='assets/backgrounds/signup.png')
  finalizeButton = PhotoImage(file='assets/components/finalizeButton.png')
  backButton = PhotoImage(file='assets/components/BackButton.png')

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

  background = PhotoImage(file='assets/backgrounds/homeplanner.png')
  editButton = PhotoImage(file='assets/components/editButton.png')
  signoutButton = PhotoImage(file='assets/components/signOutButton.png')

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
      SQL_insert_user = (
        f'INSERT INTO eventos (titulo, diaSemana) VALUES ("{valoresSunday[row]}", "sunday")'
      )
      db_user_insert(connection, SQL_insert_user)

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

  background = PhotoImage(file='assets/backgrounds/edit.png')
  confirmButton = PhotoImage(file='assets/components/confirmButton.png')

  label = Label(screen, image=background)
  label.pack()

  button_confirm = Button(screen, highlightthickness=0, bd=0, background='#4284F2', image=confirmButton, command=lambda:
    [saveDatas(),
     screen.destroy(),
     homeScreen('Microsfot - Tarefas')])
  button_confirm.place(width=36.5, height=36.5, x=91, y=122)

  sunday =   ['---', '---', '---', '---', '---', '---', '---', '---', '---', '---', '---', '---']
  monday =   ['---', '---', '---', '---', '---', '---', '---', '---', '---', '---', '---', '---']
  tuesday =  ['---', '---', '---', '---', '---', '---', '---', '---', '---', '---', '---', '---']
  wednesday =['---', '---', '---', '---', '---', '---', '---', '---', '---', '---', '---', '---']
  thursday = ['---', '---', '---', '---', '---', '---', '---', '---', '---', '---', '---', '---']
  friday =   ['---', '---', '---', '---', '---', '---', '---', '---', '---', '---', '---', '---']
  saturday = ['---', '---', '---', '---', '---', '---', '---', '---', '---', '---', '---', '---']

  y = [233, 233, 233, 233, 233, 233, 233]

  for index in range(12):
    sunday[index] = Entry(screen, highlightthickness=0, bd=1, font=('Inter', 8), justify=LEFT, foreground='#605672')
    sunday[index].place(width=98, height=23, x=153, y=y[0])
    y[0] += 33

  for index in range(12):
    monday[index] = Entry(screen, highlightthickness=0, bd=1, font=('Inter', 8), justify=LEFT, foreground='#605672')
    monday[index].place(width=98, height=23, x=299, y=y[1])
    y[1] += 33

  for index in range(12):
    monday[index] = Entry(screen, highlightthickness=0, bd=1, font=('Inter', 8), justify=LEFT, foreground='#605672')
    monday[index].place(width=98, height=23, x=445, y=y[2])
    y[2] += 33

  for index in range(12):
    monday[index] = Entry(screen, highlightthickness=0, bd=1, font=('Inter', 8), justify=LEFT, foreground='#605672')
    monday[index].place(width=98, height=23, x=591, y=y[3])
    y[3] += 33

  for index in range(12):
    monday[index] = Entry(screen, highlightthickness=0, bd=1, font=('Inter', 8), justify=LEFT, foreground='#605672')
    monday[index].place(width=98, height=23, x=737, y=y[4])
    y[4] += 33

  for index in range(12):
    monday[index] = Entry(screen, highlightthickness=0, bd=1, font=('Inter', 8), justify=LEFT, foreground='#605672')
    monday[index].place(width=98, height=23, x=883, y=y[5])
    y[5] += 33

  for index in range(12):
    monday[index] = Entry(screen, highlightthickness=0, bd=1, font=('Inter', 8), justify=LEFT, foreground='#605672')
    monday[index].place(width=98, height=23, x=1029, y=y[6])
    y[6] += 33

  screen.mainloop()


def editPassword(title):
  def enviarEmail(emailPessoa):
    global code
    code = random.randint(1111, 9999)
    corpoEmail = """
        <p>Olá! O seu código de verificação é: {}</p>
        """.format(code)

    msg = email.message.Message()
    msg['Subjecy'] = "Código para recuperação de senha"
    msg['From'] = "suporteplanner321@gmail.com"
    msg['To'] = "{}".format(emailPessoa)
    password = "okuvnwqnrqkcpbmq"
    msg.add_header('Content-Type', 'text/html')
    msg.set_payload(corpoEmail)
    s = smtplib.SMTP('smtp.gmail.com: 587')
    s.starttls()

    s.login(msg['From'], password)
    s.sendmail(msg['From'], msg['To'], msg.as_string().encode('utf-8'))
  def verificarEmail():
    connection = db_connection_start()
    SQL_search_user = "SELECT * FROM usuarios"
    users = db_search_user(connection, SQL_search_user)

    validado = False
    for user in users:
      if user[1] == input_email.get():
        enviarEmail(input_email.get())
        global emailParaRedefinicao
        emailParaRedefinicao = str(input_email.get())
        screen.destroy()
        ScreenInsertCode("Microsfot - Insira o código")
        validado = True
    if validado == False:
      messagebox.showerror("ERRO", """Ops... ocorreu um erro!
O email inserido não existe na plataforma. Verifique se a email foi escrito corretamente :)""")

    db_connection_close(connection)

  screen = Tk()
  screen.title(title)
  screen.geometry('1280x800')

  background = PhotoImage(file='assets/backgrounds/ScreenEditPassword.png')
  restoreButton = PhotoImage(file='assets/components/ButtonRestore.png')
  backButton = PhotoImage(file='assets/components/BackButton.png')


  label = Label(screen, image=background)
  label.pack()

  input_email = Entry(screen, highlightthickness=0, bd=0, font=('Inter', 8), justify=LEFT, foreground='#605672')
  input_email.place(width=370, height=32, x=172, y=353)

  button_restore = Button(screen, highlightthickness=0, bd=0, background='#4284F2', image=restoreButton, command=verificarEmail)
  button_restore.place(width=223, height=45, x=170, y=552)


  button_back = Button(screen, highlightthickness=0, bd=0, background='white', image=backButton, command=lambda:
  [
      screen.destroy(),
      signinScreen('Microsfot - Tela Inicial')
  ])
  button_back.place(width=131, height=45, x=415, y=552)



  screen.mainloop()


def ScreenInsertCode(title):
  def verificaCodigo():
    if input_code.get() == str(code):
      screen.destroy()
      ScreenNewPassword("Microsfot - Inserindo a nova senha")
    else:
      messagebox.showerror("ERRO", """Código inválido""")


  screen = Tk()
  screen.title(title)
  screen.geometry('1280x800')

  background = PhotoImage(file='assets/backgrounds/ScreenInsertCode.png')
  resetButton = PhotoImage(file='assets/components/ButtonReset.png')
  backButton = PhotoImage(file='assets/components/BackButton.png')

  label = Label(screen, image=background)
  label.pack()

  input_code = Entry(screen, highlightthickness=0, bd=0, font=('Inter', 8), justify=LEFT, foreground='#605672')
  input_code.place(width=370, height=32, x=172, y=433)


  button_reset = Button(screen, highlightthickness=0, bd=0, background='#4284F2', image=resetButton, command=verificaCodigo)
  button_reset.place(width=220, height=45, x=170, y=522)

  button_back = Button(screen, highlightthickness=0, bd=0, background='white', image=backButton, command=lambda:
  [
    screen.destroy(),
    signinScreen('Microsfot - Tela Inicial')
  ])
  button_back.place(width=131, height=45, x=413, y=522)

  screen.mainloop()


def ScreenNewPassword(title):
  def verificaSenhas():

    simbols = [
      '@', '#', '$', '%', '&',
    ]
    password = input_NewPassword
    senhaForte = False

    if input_NewPassword.get() == input_NewPasswordAgain.get():
      if len(password) >= 8:
        if password.upper() != password and password.lower() != password:
          for simbol in simbols:
            if simbol in list(password):
              senhaForte = True
              connection = db_connection_start()
              SQL_reset_password = (
                f"""
                UPDATE usuarios
                SET senha = "{input_NewPassword.get()}"
                WHERE email = "{emailParaRedefinicao}";      
                """
              )
              db_reset_password(connection, SQL_reset_password)
              db_connection_close(connection)

              messagebox.showinfo("SUCESSO", """Senha redefinida com sucesso""")
              screen.destroy()
              signinScreen('Microsfot - Tela Inicial')
          if senhaForte != True:
            messagebox.showerror("ERRO", """Senha muito fraca: Insira algum símbolo especial
            (Ex: @, #, % etc.)""")
        else:
          messagebox.showerror("ERRO", """Senha muito fraca: Insira letras maiúsculas e minúsculas""")
      else:
        messagebox.showerror("ERRO", """Senha muito fraca: Senha muito pequena""")
    else:
      messagebox.showerror("ERRO", """As senhas não coincidem""")


  screen = Tk()
  screen.title(title)
  screen.geometry('1280x800')

  background = PhotoImage(file='assets/backgrounds/ScreenNewPassword.png')
  concludeButton = PhotoImage(file='assets/components/ButtonConclude.png')

  label = Label(screen, image=background)
  label.pack()


  input_NewPassword = Entry(screen, highlightthickness=0, bd=0, font=('Inter', 8), justify=LEFT, foreground='#605672')
  input_NewPassword.place(width=370, height=32, x=172, y=340)

  input_NewPasswordAgain = Entry(screen, highlightthickness=0, bd=0, font=('Inter', 8), justify=LEFT, foreground='#605672')
  input_NewPasswordAgain.place(width=370, height=32, x=172, y=433)



  button_conclude = Button(screen, highlightthickness=0, bd=0, background='#4284F2', image=concludeButton, command=verificaSenhas)
  button_conclude.place(width=220, height=45, x=170, y=522)


  label.mainloop()
signinScreen('Microsfot - Tela Inicial')
