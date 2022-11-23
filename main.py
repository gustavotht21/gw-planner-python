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
from tkinter import *
from connection import *
from exceptions import *
from classes import Usuario
from tkinter import messagebox

def createScreens(title):
  screen = Tk()
  screen.title(title)
  screen.geometry('1280x800')
  screen.resizable(width=False, height=False)
  iconScreen = PhotoImage(file="./assets/components/IconScreen.png")
  screen.iconphoto(False, iconScreen)
  return screen

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
  background = PhotoImage(file='assets/backgrounds/loginSreen.png')
  signinButton = PhotoImage(file='assets/components/signinButton.png')
  signupButton = PhotoImage(file='assets/components/signupButton.png')
  forgetButton = PhotoImage(file='assets/components/ButtonForgetPassword.png')


  label = Label(screen, image=background)
  label.pack()

  input_email = Entry(screen, highlightthickness=0, bd=0, font=('Inter', 8), justify=LEFT, foreground='#605672')
  input_email.place(width=370, height=35, x=172, y=353)

  input_password = Entry(screen, highlightthickness=0, textvariable=hidePassword, show="*", bd=0, font=('Inter', 8), justify=LEFT, foreground='#605672')
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
      email_verification = False

      first_input = input_email.get()
      second_input = input_email_again.get()
      password = input_password.get()
      senhaForte = True

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
      if senhaForte != True:
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
  hidePassword = StringVar()
  background = PhotoImage(file='assets/backgrounds/signupScreen.png')
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
  screen = createScreens(title)

  background = PhotoImage(file='assets/backgrounds/homeScreen.png')
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

  background = PhotoImage(file='assets/backgrounds/editScreen.png')
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

def editPassword(title):
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
  background = PhotoImage(file='assets/backgrounds/ScreenEditPassword.png')
  restoreButton = PhotoImage(file='assets/components/ButtonRestore.png')
  backButton = PhotoImage(file='assets/components/BackButton.png')

  label = Label(screen, image=background)
  label.pack()

  input_email = Entry(screen, highlightthickness=0, bd=0, font=('Inter', 8), justify=LEFT, foreground='#605672')
  input_email.place(width=370, height=32, x=172, y=353)

  button_restore = Button(screen, highlightthickness=0, bd=0, background='#4284F2', image=restoreButton, command=verificarEmail)
  button_restore.place(width=223, height=45, x=170, y=552)


  button_back = Button(screen, highlightthickness=0, bd=0, background='white', image=backButton, command=lambda: [
    screen.destroy(),
    signinScreen('Microsfot - Tela Inicial')
  ])
  button_back.place(width=130, height=45, x=414, y=553)



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