class ProdutoPichau:
    def __init__(self, link, price, category: str = None, nome: str = None, link_img: str = None,
                 max_price: float = None):
        self._link = link
        self._price = price
        self._category = category
        self._shop = "Pichau"
        self._nome = nome
        self._link_img = link_img
        self._max_price = max_price

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
    def category(self):
        return self._category

    @category.setter
    def category(self, value):
        self._category = value

    @property
    def shop(self):
        return self._shop

    @shop.setter
    def shop(self, value):
        self._shop = value

    @property
    def nome(self):
        return self._nome

    @nome.setter
    def nome(self, value):
        self._nome = value

    @property
    def link_img(self):
        return self._link_img

    @link_img.setter
    def link_img(self, value):
        self._link_img = value

    @property
    def max_price(self):
        return self._max_price

    @max_price.setter
    def max_price(self, value):
        self._max_price = value

    def __str__(self):
        mensagem = (
            f'<a href="{self._link_img}">&#8205;</a>'  # Link vazio para a imagem
            f"<b>🎉 Novo produto Pichau: {self._category}</b>\n\n"
            f"<a href=\"{self._link}\">🔗 {self._nome}</a>\n\n"
            f"💰 <b>Preço:</b> R${self._price:.2f}\n\n"
            f"🛒 <b>Deseja comprar?!</b>\n"
        )
        return mensagem

    def compra_confirmada(self):
        mensagem = (
            f'<a href="{self._link_img}">&#8205;</a>\n\n'
            f"<a href=\"{self._link}\">🔗 {self._nome}</a>\n\n"
            f"💰 <b>Valor:</b> R${self._price:.2f}\n\n"
        )
        return mensagem
