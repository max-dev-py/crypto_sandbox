from .base import Robot


class CincoRobot(Robot):
    check_price = None
    data_credentials = {
        'date': 'timestamp',
        'price': 'close',
    }

    def __init__(self, buy_rate=0.95, profit_rate=1.05, save_rate=0.05, amount_rate=0.05, **kwargs):
        super().__init__(**kwargs)
        self.profit_rate = profit_rate
        self.buy_rate = buy_rate
        self.save_rate = save_rate
        self.amount_rate = amount_rate

    def apply(self, **kwargs):
        self.price = float(kwargs[self.data_credentials['price']])
        date = kwargs[self.data_credentials['date']]

        # If it's the first time: buy 1 unit and remeber the price
        if self.check_price is None:
            self.make_deal(date=date, price=self.price, quantity=self.get_deal_amount() / self.price)
            self.check_price = self.price
            self.heap = [self.deals[0]]
            return True

        # if price is below the check price for 5%: buy 1 unit more and renew check price
        if self.price < (self.check_price * self.buy_rate):
            self.make_deal(date=date, price=self.price, quantity=self.get_deal_amount() / self.price)
            self.check_price = self.price
            self.heap.append(self.deals[-1])
            return True

        if self.price > (self.check_price * self.profit_rate) and self.heap:
            self.make_deal(date=date, price=self.price, quantity=-self.heap[-1].quantity * (1 - self.save_rate))
            self.heap.pop()
            self.check_price = self.heap[-1].price if len(self.heap) > 0 else self.price
            return True

        if not self.heap:
            self.check_price = self.price

    def get_deal_amount(self):
        return self.amount * self.amount_rate
