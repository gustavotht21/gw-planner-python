class Usuario():
    def __init__(self, idUser, email, senha):
        self.idUser = idUser
        self.email = email
        self.senha = senha
    def realizarLogin(self, emailLogin, senhaLogin):
        if self.email == emailLogin and self.senha == senhaLogin:
            return print("[LOGIN REALIZADO NA CLASSE USER]")
        return print("[LOGIN FALHOU NA CLASSE USER]")
    def recuperarSenha(self):
        pass
    def getUserInformations(self):
        print(f"USER INFORMATIONS\nID: {self.idUser}\nEMAIL: {self.email}\nPASSWORD: {self.senha}")
    def getEmailUser(self):
        return self.email
    def getSenhaUser(self):
        return self.senha
    def getIdUser(self):
        return self.idUser

class Evento():
    def __init__(self, titulo, diaSemana):
        self.titulo = titulo
        self.diaSemana = diaSemana
    def editarEventos(self):
        pass
    def salvarEventos(self):
        pass