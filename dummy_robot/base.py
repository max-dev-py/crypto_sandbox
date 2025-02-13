from abc import abstractmethod
from dataclasses import dataclass
import datetime


@dataclass
class Deal:
    date: datetime.date
    quantity: float
    price: float

    @property
    def amount(self):
        return self.quantity * self.price


class Robot(object):
    price = 0.0

    def __init__(self, *args, **kwargs):
        self.amount = kwargs['amount']
        self.deals = []

    @abstractmethod
    def apply(self, *args, **kwargs):
        pass

    def get_long_deals(self):
        return [_ for _ in self.deals if _.quantity > 0]

    def get_short_deals(self):
        return [_ for _ in self.deals if _.quantity < 0]

    def make_deal(self, date, quantity, price):
        self.deals.append(Deal(date, quantity, price))
        self.amount -= price * quantity

    @abstractmethod
    def get_deal_amount(self):
        pass

    def get_quantity(self):
        return sum(
            [_.quantity for _ in self.deals]
        )

    def get_total_assets(self):
        return self.amount + self.get_quantity() * self.price

    @property
    def status(self):
        return f'Amount {self.amount}, Quantity: {self.get_quantity()}, Total: {self.get_total_assets()}'
