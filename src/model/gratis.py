class Gratis:
    def __init__(self, link, shop: str = None, nome: str = None, link_img: str = None):
        self._link = link
        self._price = 0
        self._shop = shop
        self._link_img = link_img
        self._nome = nome

    @property
    def link(self):
        return self._link

    @link.setter
    def link(self, value):
        self._link = value

    @property
    def price(self):
        return self._price

    @price.setter
    def price(self, value):
        self._price = value

    @property
    def shop(self):
        return self._shop

    @shop.setter
    def shop(self, value):
        self._shop = value

    @property
    def link_img(self):
        return self._link_img

    @link_img.setter
    def link_img(self, value):
        self._link_img = value

    @property
    def nome(self):
        return self._nome

    @nome.setter
    def nome(self, value):
        self._nome = value

    def __str__(self):
        mensagem = (
            f'<a href="{self.link_img}">&#8205;</a>'
            f"<b>🎉 Novo Produto Grátis!</b>\n\n"
            f"<a href=\"{self.link}\">🔗 {self.nome}</a>\n\n"
            f"💰 <b>Preço:</b> R${self.price:.2f}\n\n"
        )
        return mensagem
