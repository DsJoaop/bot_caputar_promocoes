class Desconto:
    def __init__(self, link, price, category: str = None, shop: str = None, nome: str = None, link_img: str = None,
                 cupom: str = None):
        self._link = link
        self._price = price
        self._shop = shop
        self._link_img = link_img
        self._nome = nome
        self._category = category
        self._cupom = cupom

    @property
    def link(self):
        return self._link

    @link.setter
    def link(self, value):
        self._link = value

    # Getter e Setter para price
    @property
    def price(self):
        return self._price

    @price.setter
    def price(self, value):
        self._price = value

    # Getter e Setter para shop
    @property
    def shop(self):
        return self._shop

    @shop.setter
    def shop(self, value):
        self._shop = value

    # Getter e Setter para link_img
    @property
    def link_img(self):
        return self._link_img

    @link_img.setter
    def link_img(self, value):
        self._link_img = value

    # Getter e Setter para nome
    @property
    def nome(self):
        return self._nome

    @nome.setter
    def nome(self, value):
        self._nome = value

    # Getter e Setter para category
    @property
    def category(self):
        return self._category

    @category.setter
    def category(self, value):
        self._category = value

    # Getter e Setter para cupom
    @property
    def cupom(self):
        return self._cupom

    @cupom.setter
    def cupom(self, value):
        self._cupom = value

    def __str__(self):
        mensagem = (
            f'<a href="{self._link_img}">&#8205;</a>'  # Link vazio para a imagem
            f"<b>🎉 Novo {self._category}</b>\n\n"
            f"<a href=\"{self._link}\">🔗 {self._nome}</a>\n\n"
            f"💰 <b>Preço:</b> R${self._price:.2f}\n\n"
        )
        return mensagem
