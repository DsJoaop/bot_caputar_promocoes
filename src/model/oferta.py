from src.model.cupom import Cupom
from src.model.desconto import Desconto
from src.model.gratis import Gratis


class Oferta:
    def __init__(self, identificador: str, desconto: Desconto = None, cupom: Cupom = None, gratis: Gratis = None):
        self._id = identificador
        self._cupom: Cupom = cupom
        self._gratis: Gratis = gratis
        self._oferta: Desconto = desconto

    @property
    def id(self) -> str:
        return self._id

    @id.setter
    def id(self, value):
        self._id = value

    def __str__(self):
        if self._cupom:
            return str(self._cupom)
        elif self._gratis:
            return str(self._gratis)
        elif self._oferta:
            return str(self._oferta)
        else:
            return f"Oferta (ID: {self._id})"
