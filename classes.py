class Usuario():
    def __init__(self, idUser, email, senha):
        self.idUser = idUser
        self.email = email
        self.senha = senha
    def AcessUserInformation(self):
        userInformation = [self.idUser, self.email, self.senha]
        return userInformation

class Evento():
    def __init__(self, idEvent, titulo, diaSemana):
        self.idEvent = idEvent
        self.titulo = titulo
        self.diaSemana = diaSemana
    def acessEventInformation(self):
        eventInformation = [self.idEvent, self.titulo, self.diaSemana]
        return eventInformation