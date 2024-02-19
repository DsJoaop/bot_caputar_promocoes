class Produto:
    def __init__(self, link, price, category=None, shop=None, nome=None, link_img=None, max_price=None):
        self._link = link
        self._price = price
        self._shop = shop
        self._link_img = link_img
        self._nome = nome
        self._max_price = max_price
        self._category = category

    @property
    def link(self):
        return self._link

    @property
    def price(self):
        return self._price

    @property
    def shop(self):
        return self._shop

    @property
    def link_img(self):
        return self._link_img

    @property
    def nome(self):
        return self._nome

    @property
    def max_price(self):
        return self._max_price

    @property
    def category(self):
        return self._category

    @link.setter
    def link(self, value):
        self._link = value

    @price.setter
    def price(self, value):
        self._price = value

    @shop.setter
    def shop(self, value):
        self._shop = value

    @link_img.setter
    def link_img(self, value):
        self._link_img = value

    @nome.setter
    def nome(self, value):
        self._nome = value

    @max_price.setter
    def max_price(self, value):
        self._max_price = value

    @category.setter
    def category(self, value):
        self._category = value
