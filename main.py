"""
PLANNER - PROJETO INTEGRADOR

----- Turma: -----
2° Ano de Informática Vespertino

----- Grupo: -----
Escorpião

----- Integrantes: -----
Alexandre Borgs Fujita
Gustavo Casagrande Borges
Wata Negreiros Monteiro
"""

import time
import random
import smtplib
import re
import sqlite3
import email.message
import tkinter
from tkinter import *
from connection import *
from exceptions import *
from classes import Usuario
from tkinter import messagebox

global language, portuguese
language = 0
portuguese = True

def createScreens(title):
  screen = Tk()
  screen.title(title)
  screen.geometry('1280x800')
  screen.resizable(width=False, height=False)
  iconScreen = PhotoImage(file="assets/components/PortugueseComponents/IconScreen.png")
  screen.iconphoto(False, iconScreen)
  return screen

def selectLanguage(name: str, type: str, item: str):
  typeTitle = type.title()
  if language == 0:
    name = PhotoImage(file=f"assets/{type}/Portuguese{typeTitle}/{item}")
  else:
    name = PhotoImage(file=f"assets/{type}/English{typeTitle}/{item}")
  return name

def signinScreen(title):
  def login():
    connection = db_connection_start()
    SQL_search_user = "SELECT * FROM usuarios"
    users = db_search_user(connection, SQL_search_user)
    validado = False

    try:
      for user in users:
        if user[1] == input_email.get() and user[2] == input_password.get():
          validado = True
          global usuarioAtual
          global userOn
          usuarioAtual = Usuario(user[0], input_email.get(), input_password.get())
          screen.destroy()
          homeScreen("Microsfot - Tarefas")
      if validado == False:
        raise ErrorCredenciaisIncorretas
    except ErrorCredenciaisIncorretas:
      messagebox.showerror("ERRO", """Erro ao tentar fazer login. Considere:
            - Ver se as informações foram escritas corretamente;
            - Cadastrar-se caso não possua conta;
            - Clicar em "Esqueceu a senha?" para recuperar sua senha, caso a tenha esquecido""")
      input_email.delete(0, END)
      input_password.delete(0, END)



    db_connection_close(connection)
  screen = createScreens(title)

  connection = db_connection_start()
  SQL_create_table = """
      CREATE TABLE IF NOT EXISTS usuarios (                  
      idUser integer PRIMARY KEY AUTOINCREMENT,

      email text NOT NULL,
      senha text NOT NULL
      ); """
  db_table_create(connection, SQL_create_table)

  hidePassword = StringVar()
  background = selectLanguage("background", "backgrounds", "loginScreen.png")
  signinButton = selectLanguage("signinButton", "components", "signinButton.png")
  signupButton = selectLanguage("signupButton", "components", "signupButton.png")
  forgetButton = selectLanguage("forgetButton", "components", "ButtonForgetPassword.png")
  configButton = PhotoImage(file="assets/components/ConfigButton.png")

  label = Label(screen, image=background)
  label.pack()

  input_email = Entry(screen, highlightthickness=0, bd=0, font=('Inter', 8), justify=LEFT, foreground='#605672')
  input_email.place(width=370, height=35, x=172, y=353)

  input_password = Entry(screen, highlightthickness=0, textvariable=hidePassword, show="*", bd=0, font=('Inter', 8), justify=LEFT, foreground='#605672')
  input_password.place(width=370, height=35, x=172, y=450)

  button_signin = Button(screen, highlightthickness=0, bd=0, background='#4284F2', image=signinButton, command=login)
  button_signin.place(width=129, height=43, x=175, y=527)

  button_signup = Button(screen, highlightthickness=0, bd=0, background='white', image=signupButton, command=lambda:
  [
      screen.destroy(),
      signupScreen('Microsfot - Cadastro')
  ])
  button_signup.place(width=184, height=41, x=330, y=528)

  button_forget = Button(screen, highlightthickness=0, bd=0, background='white', image=forgetButton, command=lambda:
  [
    screen.destroy(),
    editPassword("Microsfot - Redefinir senha", "login")
  ])
  if language == 0:
    x = 401
  else:
    x = 373
  button_forget.place(width=174, height=19, x=x, y=496)


  button_config = Button(screen, highlightthickness=0, bd=0, background='#6092E3', image=configButton, command=lambda: [
    screen.destroy(),
    configScreen('Microsfot - Configurações', "login")
    ]
  )
  button_config.place(width=64, height=64, x=1138, y=24)

  screen.mainloop()

def signupScreen(title):
  connection = db_connection_start()

  def verificationEmail():

    try:
      SQL_search_user = "SELECT email FROM usuarios"
      emails_in_database = db_search_user(connection, SQL_search_user)

      emails_extensios = [
        'ifro.edu.br', 'estudante.ifro.edu.br', 'gmail.com', 'hotmail.com',
        'yahoo.com'
      ]
      simbols = [
        '@', '#', '$', '%', '&',
      ]
      email_verification = True

      first_input = input_email.get()
      second_input = input_email_again.get()
      password = input_password.get()
      senhaForte = False

      for email in emails_in_database:
        if email[0] == first_input:
          email_verification = False

      if '@' not in list(first_input):
        raise ErrorEmailSemArroba
      if first_input.split('@')[1] not in emails_extensios:
        raise ErrorExtensaoEmailInvalido
      if email_verification == False:
        raise ErrorEmailJaUsado
      if first_input != second_input:
        raise ErrorEmailsDiferentes
      if len(password) < 8:
        raise ErrorSenhaMuitoPequena
      if password.upper() == password or password.lower() == password:
        raise ErrorSenhaSemLetra
      if bool(re.search(r'\d', password)) == False:
        raise ErrorSenhaSemNumero
      for simbol in simbols:
        if simbol in list(password):
          senhaForte = True
      if senhaForte == False:
        raise ErrorSenhaSemSimbolo

    except ErrorEmailSemArroba:
      messagebox.showerror("ERRO", "Insira um email válido.")
      input_email.delete(0, END)
      input_email_again.delete(0, END)
    except ErrorExtensaoEmailInvalido:
      messagebox.showerror("ERRO", "Insira um email válido.")
      input_email.delete(0, END)
      input_email_again.delete(0, END)

    except ErrorEmailJaUsado:
      messagebox.showerror("ERRO", "Email já cadastrado")
    except ErrorEmailsDiferentes:
      messagebox.showerror("ERRO", "Os emails devem ser iguais")
    except ErrorSenhaMuitoPequena:
      messagebox.showerror("ERRO", "Senha muito fraca: Senha muito pequena")
    except ErrorSenhaSemLetra:
      messagebox.showerror("ERRO", "Senha muito fraca: Insira letras maiúsculas e minúsculas")
    except ErrorSenhaSemNumero:
      messagebox.showerror("ERRO", "Senha muito fraca: Insira algum número")
    except ErrorSenhaSemSimbolo:
      messagebox.showerror("ERRO", "Senha muito fraca: Insira algum símbolo especial (Ex: @, #, % etc.)")
    else:
      SQL_insert_user = (
        f'INSERT INTO usuarios (email, senha) VALUES ("{first_input}","{password}")')
      db_user_insert(connection, SQL_insert_user)

      messagebox.showinfo("SUCESSO", """Conta criada com sucesso""")

      SQL_create_table = """   
          CREATE TABLE IF NOT EXISTS eventos (    
            id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
            titulo text NOT NULL,
            diaSemana text NOT NULL,
            idEventUser INTEGER NOT NULL,
            eventNumber INTEGER NOT NULL,

            FOREIGN KEY (idEventUser)
            REFERENCES usuarios (idUser)
          );"""
      db_table_create(connection, SQL_create_table)

      SQL_search_user = """SELECT idUser FROM usuarios
               ORDER BY idUser DESC
               LIMIT 1;"""
      user = db_search_user(connection, SQL_search_user)
      idUserForCreateRegister = user[0][0]
      indexEventNumber = 1
      for row in range(1, 13):
        SQL_insert_user = (
          f'INSERT INTO eventos (titulo, diaSemana, idEventUser, eventNumber) VALUES ("---","sunday", {idUserForCreateRegister}, {indexEventNumber}) '
        )
        db_user_insert(connection, SQL_insert_user)
        indexEventNumber += 1
      for row in range(13, 25):
        SQL_insert_user = (
          f'INSERT INTO eventos (titulo, diaSemana, idEventUser, eventNumber) VALUES ("---","monday", {idUserForCreateRegister}, {indexEventNumber}) '
        )
        db_user_insert(connection, SQL_insert_user)
        indexEventNumber += 1
      for row in range(25, 37):
        SQL_insert_user = (
          f'INSERT INTO eventos (titulo, diaSemana, idEventUser, eventNumber) VALUES ("---","tuesday", {idUserForCreateRegister}, {indexEventNumber}) '
        )
        db_user_insert(connection, SQL_insert_user)
        indexEventNumber += 1
      for row in range(37, 49):
        SQL_insert_user = (
          f'INSERT INTO eventos (titulo, diaSemana, idEventUser, eventNumber) VALUES ("---","wednesday", {idUserForCreateRegister}, {indexEventNumber}) '
        )
        db_user_insert(connection, SQL_insert_user)
        indexEventNumber += 1
      for row in range(49, 61):
        SQL_insert_user = (
          f'INSERT INTO eventos (titulo, diaSemana, idEventUser, eventNumber) VALUES ("---","thursday", {idUserForCreateRegister}, {indexEventNumber}) '
        )
        db_user_insert(connection, SQL_insert_user)
        indexEventNumber += 1
      for row in range(61, 73):
        SQL_insert_user = (
          f'INSERT INTO eventos (titulo, diaSemana, idEventUser, eventNumber) VALUES ("---","friday", {idUserForCreateRegister}, {indexEventNumber}) '
        )
        db_user_insert(connection, SQL_insert_user)
        indexEventNumber += 1
      for row in range(73, 85):
        SQL_insert_user = (
          f'INSERT INTO eventos (titulo, diaSemana, idEventUser, eventNumber) VALUES ("---","saturday", {idUserForCreateRegister}, {indexEventNumber}) '
        )
        db_user_insert(connection, SQL_insert_user)
        indexEventNumber += 1
      db_connection_close(connection)

      time.sleep(0.5)
      screen.destroy(),
      signinScreen('Microsfot - Login')

  screen = createScreens(title)

  background = selectLanguage("background", "backgrounds", "signupScreen.png")
  finalizeButton = selectLanguage("finalizeButton", "components", "finalizeButton.png")
  backButton = selectLanguage("backButton", "components", "BackButton.png")
  configButton = PhotoImage(file="assets/components/ConfigButton.png")

  label = Label(screen, image=background)
  label.pack()

  input_email = Entry(screen, highlightthickness=0, bd=0, font=('Inter', 8), justify=LEFT, foreground='#605672')
  input_email.place(width=370, height=35, x=172, y=328)

  input_email_again = Entry(screen, highlightthickness=0, bd=0, font=('Inter', 8), justify=LEFT, foreground='#605672')
  input_email_again.place(width=370, height=35, x=172, y=393)

  input_password = Entry(screen, highlightthickness=0, bd=0, font=('Inter', 8), justify=LEFT, foreground='#605672')
  input_password.place(width=370, height=35, x=172, y=458)

  button_signup = Button(screen, highlightthickness=0, bd=0, background='#4284F2', image=finalizeButton, command=verificationEmail)
  button_signup.place(width=220, height=41, x=172, y=538)

  button_back = Button(screen, highlightthickness=0, bd=0, background='white', image=backButton, command=lambda:
  [
      screen.destroy(),
      signinScreen('Microsfot - Tela Inicial')
  ])
  button_back.place(width=121, height=41, x=420, y=538)

  button_config = Button(screen, highlightthickness=0, bd=0, background='#6092E3', image=configButton, command=lambda: [
    screen.destroy(),
    configScreen('Microsfot - Configurações', "cadastro")
    ]
  )
  button_config.place(width=64, height=64, x=1138, y=24)

  screen.mainloop()

def homeScreen(title):
  screen = createScreens(title)

  background = selectLanguage("background", "backgrounds", "homeScreen.png")
  editButton = PhotoImage(file='assets/components/editButton.png')
  signoutButton = selectLanguage("signoutButton", "components", "SignOutButton.png")
  informationButton = selectLanguage("informationButton", "components", "InformationButton.png")
  configButton = PhotoImage(file="assets/components/ConfigButton.png")

  label = Label(screen, image=background)
  label.pack()

  button_edit = Button(screen, highlightthickness=0, bd=0, background='#4284F2', image=editButton, command=lambda:
    [screen.destroy(),
     editScreen('Microsfot - Editar Tarefas')])
  button_edit.place(width=36.5, height=36.5, x=91, y=122)

  button_signout = Button(screen, highlightthickness=0, bd=0, background='#719DE4', image=signoutButton, command=lambda:
  [
      screen.destroy(),
      signinScreen('Microsfot - Tela Inicial')
  ])
  button_signout.place(width=108, height=41, x=1092, y=724)

  button_information = Button(screen, highlightthickness=0, bd=0, background='#4B84E1', image=informationButton, command=lambda: [
    screen.destroy(),
    userInformationScreen('Microsfot - Informações pessoais')
    ]
  )
  button_information.place(width=234, height=41, x=81, y=724)


  button_config = Button(screen, highlightthickness=0, bd=0, background='#6092E3', image=configButton, command=lambda: [
    screen.destroy(),
    configScreen('Microsfot - Configurações', "home")
    ]
  )
  button_config.place(width=64, height=64, x=1138, y=24)

  connection = db_connection_start()

  idUsuarioAtual = (usuarioAtual.AcessUserInformation())[0]
  SQL_search_events = f'SELECT titulo FROM eventos where idEventUser == {idUsuarioAtual}'
  events = db_search_events(connection, SQL_search_events)

  labels_texts = []
  for event in events:
    labels_texts.append(event[0])

  y = [233, 233, 233, 233, 233, 233, 233]
  for index in range(12):
    sunday_label = Label(screen, text=labels_texts[index], background='white')
    sunday_label.place(width=98, height=23, x=153, y=y[0])
    y[0] += 33

  for index in range(12,24):
    monday_label = Label(screen, text=labels_texts[index], background='white')
    monday_label.place(width=98, height=23, x=299, y=y[1])
    y[1] += 33

  for index in range(24,36):
    tuesday_label = Label(screen, text=labels_texts[index], background='white')
    tuesday_label.place(width=98, height=23, x=445, y=y[2])
    y[2] += 33

  for index in range(36,48):
    wednesday_label = Label(screen, text=labels_texts[index], background='white')
    wednesday_label.place(width=98, height=23, x=591, y=y[3])
    y[3] += 33

  for index in range(48,60):
    thursday_label = Label(screen, text=labels_texts[index], background='white')
    thursday_label.place(width=98, height=23, x=737, y=y[4])
    y[4] += 33

  for index in range(60,72):
    friday_label = Label(screen, text=labels_texts[index], background='white')
    friday_label.place(width=98, height=23, x=883, y=y[5])
    y[5] += 33

  for index in range(72,84):
    saturday_label = Label(screen, text=labels_texts[index], background='white')
    saturday_label.place(width=98, height=23, x=1029, y=y[6])
    y[6] += 33

  screen.mainloop()
  db_connection_close(connection)

def editScreen(title):
  def saveDatas():
    connection = db_connection_start()

    idUsuarioAtual = (usuarioAtual.AcessUserInformation())[0]

    indexForUpdateDays = 0
    for row in range(1, 13):
      SQL_insert_user = (
        f'UPDATE eventos SET titulo = "{sunday[indexForUpdateDays].get()}", diaSemana = "sunday" WHERE eventNumber == {row} and idEventUser == {idUsuarioAtual}'
      )
      db_user_insert(connection, SQL_insert_user)
      indexForUpdateDays += 1
    indexForUpdateDays = 0
    for row in range(13, 25):
      SQL_insert_user = (
        f'UPDATE eventos SET titulo = "{monday[indexForUpdateDays].get()}", diaSemana = "monday" WHERE eventNumber == {row} and idEventUser == {idUsuarioAtual}'
      )
      db_user_insert(connection, SQL_insert_user)
      indexForUpdateDays += 1
    indexForUpdateDays = 0
    for row in range(25, 37):
      SQL_insert_user = (
        f'UPDATE eventos SET titulo = "{tuesday[indexForUpdateDays].get()}", diaSemana = "tuesday" WHERE eventNumber == {row} and idEventUser == {idUsuarioAtual}'
      )
      db_user_insert(connection, SQL_insert_user)
      indexForUpdateDays += 1
    indexForUpdateDays = 0
    for row in range(37, 49):
      SQL_insert_user = (
        f'UPDATE eventos SET titulo = "{wednesday[indexForUpdateDays].get()}", diaSemana = "wednesday" WHERE eventNumber == {row} and idEventUser == {idUsuarioAtual}'
      )
      db_user_insert(connection, SQL_insert_user)
      indexForUpdateDays += 1
    indexForUpdateDays = 0
    for row in range(49, 61):
      SQL_insert_user = (
        f'UPDATE eventos SET titulo = "{thursday[indexForUpdateDays].get()}", diaSemana = "thursday" WHERE eventNumber == {row} and idEventUser == {idUsuarioAtual}'
      )
      db_user_insert(connection, SQL_insert_user)
      indexForUpdateDays += 1
    indexForUpdateDays = 0
    for row in range(61, 73):
      SQL_insert_user = (
        f'UPDATE eventos SET titulo = "{friday[indexForUpdateDays].get()}", diaSemana = "friday" WHERE eventNumber == {row} and idEventUser == {idUsuarioAtual}'
      )
      db_user_insert(connection, SQL_insert_user)
      indexForUpdateDays += 1
    indexForUpdateDays = 0
    for row in range(73, 85):
      SQL_insert_user = (
        f'UPDATE eventos SET titulo = "{saturday[indexForUpdateDays].get()}", diaSemana = "saturday" WHERE eventNumber == {row} and idEventUser == {idUsuarioAtual}'
      )
      db_user_insert(connection, SQL_insert_user)
      indexForUpdateDays += 1


    db_connection_close(connection)
  screen = createScreens(title)

  background = selectLanguage("background", "backgrounds", "editScreen.png")
  confirmButton = PhotoImage(file='assets/components/confirmButton.png')

  label = Label(screen, image=background)
  label.pack()

  button_confirm = Button(screen, highlightthickness=0, bd=0, background='#4284F2', image=confirmButton, command=lambda:
    [saveDatas(),
     screen.destroy(),
     homeScreen('Microsfot - Tarefas')])
  button_confirm.place(width=36.5, height=36.5, x=91, y=122)

  sunday =   ['🔴', '🟩🟩🟩', '🟩🟩🟩','',' 🟩🟩🟩', '','','', '', '', '',  '']
  monday =   ['',   '🟩', '', '🟩', '🟩', '🟩', '🟩','', '', '', '', ''       ]
  tuesday =  ['🟩', '🟩', '', '🟩', '🟩', '🟩', '🟩','', '', '', '', ''       ]
  wednesday =['🟩', '🟩🟩🟩', '🟩🟩🟩','','🟩', '🟩', '','', '', '', '', ''   ]
  thursday = ['🟩', '🟩', '', '🟩', '🟩', '🟩', '🟩','', '', '', '', ''       ]
  friday =   ['🟩', '🟩', '', '🟩', '🟩', '🟩', '🟩','', '', '', '', ''       ]
  saturday = ['🟩', '🟩', '', '🟩', '🟩', '  🟩🟩','','', '', '', '', ''      ]
  connection = db_connection_start()

  idUsuarioAtual = (usuarioAtual.AcessUserInformation())[0]
  listTitles = []

  SQL_search_events = f'SELECT * FROM eventos where idEventUser == {idUsuarioAtual}'
  events = db_search_events(connection, SQL_search_events)

  for event in events:
    print(event[1])
    listTitles.append(event[1])

  indexForEvents = 0
  db_connection_close(connection)

  y = [233, 233, 233, 233, 233, 233, 233]
  for index in range(1, 13):
    sunday[index-1] = Entry(screen, highlightthickness=0, bd=0, font=('Inter', 8), justify=CENTER, foreground='#605672')
    sunday[index-1].place(width=98, height=23, x=153, y=y[0])
    sunday[index-1].insert(0, listTitles[indexForEvents])
    indexForEvents += 1
    y[0] += 33
  for index in range(1, 13):
    monday[index-1] = Entry(screen, highlightthickness=0, bd=0, font=('Inter', 8), justify=CENTER, foreground='#605672')
    monday[index-1].place(width=98, height=23, x=299, y=y[1])
    monday[index-1].insert(0, listTitles[indexForEvents])
    indexForEvents += 1
    y[1] += 33

  for index in range(1, 13):
    tuesday[index-1] = Entry(screen, highlightthickness=0, bd=0, font=('Inter', 8), justify=CENTER, foreground='#605672')
    tuesday[index-1].place(width=98, height=23, x=445, y=y[2])
    tuesday[index-1].insert(0, listTitles[indexForEvents])
    indexForEvents += 1
    y[2] += 33
  for index in range(1, 13):
    wednesday[index-1] = Entry(screen, highlightthickness=0, bd=0, font=('Inter', 8), justify=CENTER, foreground='#605672')
    wednesday[index-1].place(width=98, height=23, x=591, y=y[3])
    wednesday[index-1].insert(0, listTitles[indexForEvents])
    indexForEvents += 1
    y[3] += 33
  for index in range(1, 13):
    thursday[index-1] = Entry(screen, highlightthickness=0, bd=0, font=('Inter', 8), justify=CENTER, foreground='#605672')
    thursday[index-1].place(width=98, height=23, x=737, y=y[4])
    thursday[index-1].insert(0, listTitles[indexForEvents])
    indexForEvents += 1
    y[4] += 33
  for index in range(1, 13):
    friday[index-1] = Entry(screen, highlightthickness=0, bd=0, font=('Inter', 8), justify=CENTER, foreground='#605672')
    friday[index-1].place(width=98, height=23, x=883, y=y[5])
    friday[index-1].insert(0, listTitles[indexForEvents])
    indexForEvents += 1
    y[5] += 33
  for index in range(1, 13):
    saturday[index-1] = Entry(screen, highlightthickness=0, bd=0, font=('Inter', 8), justify=CENTER, foreground='#605672')
    saturday[index-1].place(width=98, height=23, x=1029, y=y[6])
    saturday[index-1].insert(0, listTitles[indexForEvents])
    indexForEvents += 1
    y[6] += 33
  screen.mainloop()

def editPassword(title, redirect):
  def enviarEmail(emailPessoa):
    global code
    code = random.randint(100000, 999999)
    corpoEmail = """
             <div style="border: 2px solid #d4deee; width: 600px; margin: 0 auto; border-radius: 10px;">
                <div style="padding: 15px;">
                  <p style="font-family: Arial; font-size: 1rem;" align="center">Olá! Aqui é o suporte do Planner Microsfot. Você solicitou uma <span style="color: #2563EB">recuperação de senha na sua conta no planner digital</span>. Seu código de verificação é:</p>
                  <p style="font-family: Arial; font-size: 1rem; font-weight: bold;" align="center"> > > > {} < < < </p>
        
                  <p style="font-family: Arial; font-size: 1rem;" align="center">Se você não solicitou essa redefinição, <span style="color: #1E3A8A;">ignore este e-mail</span>. Sua senha permanecerá a mesma.</p>

                  <p style="font-family: Arial; font-size: 1rem;" align="center">Email automático. Por favor não responda.</p>
                </div>
            </div>
        """.format(code)

    msg = email.message.Message()
    msg['Subject'] = "Código para recuperação de senha"
    msg['From'] = "plannersuportecliente123@gmail.com"
    msg['To'] = "{}".format(emailPessoa)
    password = "owyqxpganiwvnjxv"
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
    try:
      for user in users:
        if user[1] == input_email.get():
          validado = True
      if validado == False:
        raise ErrorEmailInexistente
    except ErrorEmailInexistente:
      messagebox.showerror("ERRO",
                           """Ops... ocorreu um erro! O email inserido não existe na plataforma. Verifique se a email foi escrito corretamente :)""")
    else:
      enviarEmail(input_email.get())
      global emailParaRedefinicao
      emailParaRedefinicao = str(input_email.get())
      screen.destroy()
      ScreenInsertCode("Microsfot - Insira o código")
    db_connection_close(connection)

  screen = createScreens(title)

  background = selectLanguage("background", "backgrounds", "ScreenEditPassword.png")
  restoreButton = selectLanguage("restoreButton", "components", "ButtonRestore.png")
  backButton = selectLanguage("backButton", "components", "BackButton.png")

  label = Label(screen, image=background)
  label.pack()

  input_email = Entry(screen, highlightthickness=0, bd=0, font=('Inter', 8), justify=LEFT, foreground='#605672')
  input_email.place(width=370, height=32, x=172, y=353)

  button_restore = Button(screen, highlightthickness=0, bd=0, background='#4284F2', image=restoreButton, command=verificarEmail)
  button_restore.place(width=213, height=43, x=175, y=553)

  if redirect == "login":
    button_back = Button(screen, highlightthickness=0, bd=0, background='white', image=backButton, command=lambda: [
      screen.destroy(),
      signinScreen('Microsfot - Tela Inicial')
    ])
    button_back.place(width=120, height=43, x=419, y=553)
  elif redirect == "informações":
    button_back = Button(screen, highlightthickness=0, bd=0, background='white', image=backButton, command=lambda: [
      screen.destroy(),
      userInformationScreen('Microsfot - Suas Informações')
    ])
    button_back.place(width=120, height=43, x=419, y=553)



  screen.mainloop()

def ScreenInsertCode(title):
  def verificaCodigo():
    try:
      if input_code.get() != str(code):
        raise ErrorCodigoInvalido
    except ErrorCodigoInvalido:
      messagebox.showerror("ERRO", """Código inválido""")
    else:
      screen.destroy()
      ScreenNewPassword("Microsfot - Inserindo a nova senha")

  screen = createScreens(title)


  background = selectLanguage("background", "backgrounds", "ScreenInsertCode.png")
  resetButton = selectLanguage("resetButton", "components", "ButtonReset.png")
  backButton = selectLanguage("backButton", "components", "BackButton.png")

  label = Label(screen, image=background)
  label.pack()

  input_code = Entry(screen, highlightthickness=0, bd=0, font=('Inter', 8), justify=LEFT, foreground='#605672')
  input_code.place(width=370, height=32, x=172, y=433)


  button_reset = Button(screen, highlightthickness=0, bd=0, background='#4284F2', image=resetButton, command=verificaCodigo)
  button_reset.place(width=210, height=45, x=175, y=522)

  button_back = Button(screen, highlightthickness=0, bd=0, background='white', image=backButton, command=lambda:
  [
    screen.destroy(),
    signinScreen('Microsfot - Tela Inicial')
  ])
  button_back.place(width=120, height=43, x=418, y=523)

  screen.mainloop()

def ScreenNewPassword(title):
  def verificaSenhas():
    try:
      simbols = [
        '@', '#', '$', '%', '&',
      ]
      password = input_NewPassword.get()
      senhaForte = False
      if input_NewPassword.get() != input_NewPasswordAgain.get():
        raise ErrorSenhasNaoCoincidem
      if len(password) < 8:
        raise ErrorSenhaMuitoPequena
      if password.upper() == password or password.lower() == password:
        raise ErrorSenhaSemLetra
      if bool(re.search(r'\d', password)) == False:
        raise ErrorSenhaSemNumero
      for simbol in simbols:
        if simbol in list(password):
          senhaForte = True
      if senhaForte != True:
        raise ErrorSenhaSemSimbolo

    except ErrorSenhasNaoCoincidem:
      messagebox.showerror("ERRO", """As senhas não coincidem""")
    except ErrorSenhaMuitoPequena:
      messagebox.showerror("ERRO", """Senha muito fraca: Senha muito pequena""")
    except ErrorSenhaSemLetra:
      messagebox.showerror("ERRO", """Senha muito fraca: Insira letras maiúsculas e minúsculas""")
    except ErrorSenhaSemNumero:
      messagebox.showerror("ERRO", "Senha muito fraca: Insira algum número")
    except ErrorSenhaSemSimbolo:
      messagebox.showerror("ERRO", """Senha muito fraca: Insira algum símbolo especial (Ex: @, #, % etc.)""")
    else:
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

  screen = createScreens(title)

  background = selectLanguage("background", "backgrounds", "ScreenNewPassword.png")
  concludeButton = selectLanguage("concludeButton", "components", "ButtonConclude.png")
  backButton = selectLanguage("backButton", "components", "BackButton.png")

  label = Label(screen, image=background)
  label.pack()


  input_NewPassword = Entry(screen, highlightthickness=0, bd=0, font=('Inter', 8), justify=LEFT, foreground='#605672')
  input_NewPassword.place(width=370, height=32, x=172, y=340)

  input_NewPasswordAgain = Entry(screen, highlightthickness=0, bd=0, font=('Inter', 8), justify=LEFT, foreground='#605672')
  input_NewPasswordAgain.place(width=370, height=32, x=172, y=433)



  button_conclude = Button(screen, highlightthickness=0, bd=0, background='#4284F2', image=concludeButton, command=verificaSenhas)
  button_conclude.place(width=210, height=43, x=175, y=523)

  button_back = Button(screen, highlightthickness=0, bd=0, background='white', image=backButton, command=lambda:
  [
    screen.destroy(),
    signinScreen('Microsfot - Tela Inicial')
  ])
  button_back.place(width=120, height=43, x=420, y=523)

  label.mainloop()

def userInformationScreen(title):
  screen = createScreens(title)

  information = usuarioAtual.AcessUserInformation()


  background = PhotoImage(file='assets/backgrounds/PortugueseBackgrounds/PersonalInformationScreen.png')
  backButton = PhotoImage(file='assets/components/PortugueseComponents/BackButton.png')
  resetButton = PhotoImage(file='assets/components/PortugueseComponents/RedefinirButton.png')

  label = Label(screen, image=background)
  label.pack()

  button_back = Button(screen, highlightthickness=0, bd=0, background='white', image=backButton, command=lambda:
  [
      screen.destroy(),
      homeScreen('Microsfot - Suas atividades')
  ])
  button_back.place(width=121, height=43, x=485, y=602)


  UserName = Label(screen, text="BeautifulUser", font=('Inter', 12), background="#FFFFFF")
  UserName.place(x=168, y=351)

  UserEmail = Label(screen, text=information[1], font=('Inter', 12), background="#FFFFFF")
  UserEmail.place(x=168, y=429)

  password = "********"

  userPassword = Label(screen, text=password, font=('Inter', 12), background="#FFFFFF")
  userPassword.place(x=168, y=507)

  reset_Button = Button(screen, highlightthickness=0, bd=0, background='#FFFFFF', image=resetButton, command=lambda: [
    screen.destroy(),
    editPassword("Microsfot - Redefinir senha", "informações")
  ])
  reset_Button.place(x=170, y=531)



  screen.mainloop()

def configScreen(title, redirect):
  print(portuguese)
  def item_selected(selected):
    global language
    global portuguese

    if selected == "portuguese_to_english":
      messagebox.showinfo("SUCESS", "Language changed successfully. Click on the blue button to see the changes")
      language = 1
      portuguese = False
    else:
      messagebox.showinfo("SUCESSO", "Idioma alterado com sucesso. Clique no botão azul para ver as mudanças")
      language = 0
      portuguese = True
  def resetOptions():
    global language
    if language == 1:
      messagebox.showinfo("SUCESS", "System settings reset. Click on the blue button to see the changes")
    elif language == 0:
      messagebox.showinfo("SUCESSO", "Configurações do sistema redefinidas. Clique no botão azul para ver as mudanças")
      language = 0
  screen = createScreens(title)
  backupLanguage = language


  # Images for the window
  background = selectLanguage("background", "backgrounds", "configScreen.png")
  ButtonConclude = selectLanguage("ButtonConclude", "components", "ConcludeButtonConfig.png")
  ButtonCancel = selectLanguage("ButtonCancel", "components", "ButtonCancelConfig.png")

  if portuguese == 1:
    portugueseButton = PhotoImage(file="assets/components/TruePortugueseConfigButton.png")
    englishButton = PhotoImage(file="assets/components/FalseEnglishConfigButton.png")
  else:
    portugueseButton = PhotoImage(file="assets/components/FalsePortugueseConfigButton.png")
    englishButton = PhotoImage(file="assets/components/TrueEnglishConfigButton.png")

  label = Label(screen, image=background)
  label.pack()

  PortugueseButton = Button(screen, highlightthickness=0, bd=0, background='white', image=portugueseButton, command=lambda: [
    item_selected("english_to_portuguese")
  ])
  PortugueseButton.place(width=124, height=25, x=163, y=425)

  EnglishButton = Button(screen, highlightthickness=0, bd=0, background='white', image=englishButton, command=lambda: [
    item_selected("portuguese_to_english")
  ])
  EnglishButton.place(width=124, height=25, x=163, y=454)

  if redirect == "home":
    button_conclude = Button(screen, highlightthickness=0, bd=0, background='#4284F2', image=ButtonConclude, command=lambda:
      [screen.destroy(),
       homeScreen('Microsfot - Suas tarefas')])
    button_conclude.place(width=188, height=35, x=171, y=531)
  elif redirect == "login":
    button_conclude = Button(screen, highlightthickness=0, bd=0, background='#4284F2', image=ButtonConclude, command=lambda:
      [screen.destroy(),
       signinScreen('Microsfot - Tela inicial')])
    button_conclude.place(width=188, height=35, x=171, y=531)
  elif redirect == "cadastro":
    button_conclude = Button(screen, highlightthickness=0, bd=0, background='#4284F2', image=ButtonConclude, command=lambda:
      [screen.destroy(),
       signupScreen('Microsfot - Cadastro')])
    button_conclude.place(width=188, height=35, x=171, y=531)


  button_cancel = Button(screen, highlightthickness=0, bd=0, background='white', image=ButtonCancel, command=resetOptions)
  button_cancel.place(width=155, height=39, x=383, y=528)
  screen.mainloop()



signinScreen('Microsfot - Tela inicial')