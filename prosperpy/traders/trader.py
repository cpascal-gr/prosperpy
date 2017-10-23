import decimal
import logging

import prosperpy

LOGGER = logging.getLogger(__name__)


class Trader:
    def __init__(self, product, feed, api, investment=decimal.Decimal('100'), recurring=decimal.Decimal('10')):
        self.product = product
        self.feed = feed
        self.api = api
        self.investment = investment
        self.recurring = recurring
        self.liquidity = self.investment
        self.buys = 0
        self.sells = 0
        self.positions = []

    def initialize(self):
        raise NotImplementedError()

    def clean_positions(self):
        self.positions = [position for position in self.positions if position.amount > 0]

    def return_on_investment(self):
        liquidity = self.liquidity + sum([self.feed.price * position.amount for position in self.positions])
        return liquidity * 100 / self.investment

    def __str__(self):
        return '{}<{}>'.format(self.__class__.__name__, str(self.feed))

    def buy(self):
        self.liquidity += self.recurring
        self.investment += self.recurring

        if self.liquidity:
            position = prosperpy.Position(self.product, self.liquidity / self.feed.price, self.feed.price)
            LOGGER.info('{} Buy (Price: {:.2f}) {:.8f}'.format(self, self.feed.price, position.amount))
            self.liquidity = decimal.Decimal('0')
            self.buys += 1
            self.positions.append(position)
            self.summary()

    def sell(self):
        for position in self.positions:
            profit = position.amount * self.feed.price
            profit -= profit * decimal.Decimal('0.025')

            if position.amount > 0 and profit > position.price * position.amount:
                LOGGER.info('{} Sell (Price: {:.2f}) {:.8f}'.format(self, self.feed.price, position.amount))
                self.liquidity += profit
                self.sells += 1
                position.amount = decimal.Decimal('0')
                self.summary()

        self.clean_positions()

    def summary(self):
        LOGGER.info('{} {:.2f}% ({},{})'.format(self, self.return_on_investment(), self.buys, self.sells))

    def add(self, candle):
        raise NotImplementedError()

    def trade(self):
        raise NotImplementedError()