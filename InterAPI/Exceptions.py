class BaseError(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)


class PagadorInvalido(BaseError):
    pass


class MuitasLinhas(BaseError):
    pass


class DescontoInvalido(BaseError):
    pass


class MultaInvalida(BaseError):
    pass


class MuitosCaracteres(BaseError):
    pass


class MoraInvalida(BaseError):
    pass
