class Cupom:
    def __init__(self, link: str, link_img: str, loja: str, descricao: str, codigo: str = None, desconto: str = None):
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
    def desconto(self) -> str:
        return self._desconto

    @desconto.setter
    def desconto(self, value: str):
        self._desconto = value

    def __str__(self):
        if self._codigo:
            mensagem = (
                f'<a href="{self._link_img}">&#8205;</a>'
                f"<b>🎉 Cupom {self._loja}</b>\n\n"
                f"<p>🧷 {self._descricao}</p>\n\n"
                f"<b>💰 Valor:</b> R${self._desconto}\n\n"
                f"<b>ℹ️ Código:</b> <code>{self._codigo}</code>\n\n"
                f"<a href=\"{self._link}\">🔗 Link</a>\n\n"
            )
        else:
            mensagem = (
                f'<a href="{self._link_img}">&#8205;</a>'
                f"<b>🎉 Cupom {self._loja}</b>\n\n"
                f"<p>🧷 {self._descricao}</p>\n\n"
                f"<b>💰 Valor:</b> R${self._desconto}\n\n"
                f"<a href=\"{self._link}\">🔗 Link</a>\n\n"
            )
        return mensagem
