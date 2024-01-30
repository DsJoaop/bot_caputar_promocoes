class Produto:
    def __init__(self, link, price, category=None, nome=None, link_img=None, max_price=None):
        self.link = link
        self.price = price
        self.category = category
        self.link_img = link_img
        self.nome = nome
        self.max_price = max_price
