class Cupom:
    def __init__(self, link: str, link_img: str, loja: str, descricao: str, codigo: str = None, desconto: float = None):
        self._link = link
        self._link_img = link_img
        self._loja = loja
        self._descricao = descricao
        self._codigo = codigo
        self._desconto = desconto

    @property
    def link(self) -> str:
        return self._link

    @link.setter
    def link(self, value: str):
        self._link = value

    @property
    def link_img(self) -> str:
        return self._link_img

    @link_img.setter
    def link_img(self, value: str):
        self._link_img = value

    @property
    def loja(self) -> str:
        return self._loja

    @loja.setter
    def loja(self, value: str):
        self._loja = value

    @property
    def descricao(self) -> str:
        return self._descricao

    @descricao.setter
    def descricao(self, value: str):
        self._descricao = value

    @property
    def codigo(self) -> str:
        return self._codigo

    @codigo.setter
    def codigo(self, value: str):
        self._codigo = value

    @property
    def desconto(self) -> float:
        return self._desconto

    @desconto.setter
    def desconto(self, value: float):
        self._desconto = value

    def __str__(self):
        if self.codigo:
            mensagem = (
                f'<a href="{self.link_img}">&#8205;</a>'
                f"<b>🎉 Novo cupom {self.loja}</b>\n\n"
                f"<b>🧷 Descrição: {self.descricao}</b>\n\n"
                f"<a href=\"{self.link}\">🔗 pegue aqui!</a>\n\n"
                f"💰 <b>Valor:</b> R${self.desconto:.2f} desconto\n\n"
                f"🛒 <b>ℹ️ Copie o código:</b> <code>{self.codigo:.2f}</code>\n\n"
            )
        else:
            mensagem = (
                f'<a href="{self.link_img}">&#8205;</a>'
                f"<b>🎉 Novo cupom {self.loja}</b>\n\n"
                f'<b>🧷 Descrição:</b>\n{self.descricao}\n\n'
                f"<a href=\"{self.link}\">🔗 pegue aqui!</a>\n\n"
                f"💰 <b>Valor:</b> R${self.desconto:.2f} desconto\n\n"
            )
        return mensagem
