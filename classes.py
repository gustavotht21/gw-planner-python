class Usuario():
    def __init__(self, email, senha):
        self.email = email
        self.senha = senha
    def realizarLogin(self, emailLogin, senhaLogin, userObjects):
        for user in userObjects:
            if user.email == emailLogin and user.senha == senhaLogin:
                return print("Login realizado")
        return print("Login falhou")
    def recuperarSenha(self):
        pass
    def getUserInformations(self):
        print(f"EMAIL: {self.email}\nPASSWORD: {self.senha}")

class Evento():
    def __init__(self, titulo, diaSemana):
        self.titulo = titulo
        self.diaSemana = diaSemana
    def editarEventos(self):
        pass
    def salvarEventos(self):
        pass