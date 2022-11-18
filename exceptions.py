# Exceptions para o cadastro de usuário (Referentes a senhas também podem ser usadas na redefinição de senha)
class ErrorEmailSemArroba(Exception):
    pass

class ErrorExtensaoEmailInvalido(Exception):
    pass

class ErrorEmailJaUsado(Exception):
    pass

class ErrorEmailsDiferentes(Exception):
    pass

class ErrorSenhaMuitoPequena(Exception):
    pass

class ErrorSenhaSemLetra(Exception):
    pass

class ErrorSenhaSemSimbolo(Exception):
    pass

# Exceptions para o login do usuário
class ErrorCredenciaisIncorretas(Exception):
    pass

# Exceptions para redefinição de senha do usuário
class ErrorEmailInexistente(Exception):
    pass

class ErrorCodigoInvalido(Exception):
    pass

class ErrorSenhasNaoCoincidem(Exception):
    pass
