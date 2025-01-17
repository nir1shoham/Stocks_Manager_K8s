class Stock:
    def __init__(self, id, symbol, purchasePrice, shares, name="NA", purchaseDate="NA"):
        self.id = str(id)
        self.name = str(name)
        self.symbol = str(symbol)
        self.purchasePrice = round(purchasePrice, 2)
        self.purchaseDate = str(purchaseDate)
        self.shares = int(shares)

    def json(self):
        return {
            'id': self.id,
            'name': self.name,
            'symbol': self.symbol,
            'purchase price': self.purchasePrice,
            'purchase date': self.purchaseDate,
            'shares': self.shares
        }