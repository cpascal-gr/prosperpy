import decimal
import logging

from .adx import ADXTrader

LOGGER = logging.getLogger(__name__)


class PercentageTrader(ADXTrader):
    def __init__(self, percentage, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.percentage = percentage

    def __str__(self):
        return '{}{}<{}>'.format(self.__class__.__name__, self.percentage, str(self.feed))

    def sell(self):
        for position in self.positions:
            profit = position.amount * self.feed.price
            profit -= profit * decimal.Decimal('0.025')

            if position.amount > 0 and profit > position.price * position.amount:
                if position.amount < decimal.Decimal('0.0000001'):
                    LOGGER.info('%s Liquidating (Price: %s) %s', self, self.feed.price, position.amount)
                    self.liquidity += profit
                    self.sells += 1
                    position.amount = decimal.Decimal('0')
                else:
                    profit = profit * self.percentage
                    LOGGER.info('%s Sell (Price: %s) %s', self, self.feed.price, position.amount)
                    self.liquidity += profit
                    position.amount *= decimal.Decimal('1') - self.percentage
                    self.sells += 1

        self.clean_positions()
