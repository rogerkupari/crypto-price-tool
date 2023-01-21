import logging
import datetime
from gecko_interface import GeckoItem


class Transaction:
    __logger = None
    __exchanger = None
    __coin_symbol = None
    __transaction_time = None
    __operation = None
    __change = None
    __event_nbr = None
    __gecko = None
    __note = None

    def __init__(self, exchanger, coin_symbol, transaction_time, operation, change, event_nbr):
        logging.config.fileConfig('conf/log.conf')
        self.__logger = logging.getLogger(type(self).__name__)

        self.__exchanger = exchanger
        self.__coin_symbol = coin_symbol
        self.__transaction_time = transaction_time
        self.__operation = operation
        self.__change = change
        self.__event_nbr = event_nbr
        self.__gecko = GeckoItem(
            datetime.datetime.strptime(transaction_time, '%Y-%m-%d %H:%M:%S').strftime('%d-%m-%Y'), coin_symbol)
        self.__logger.debug("args(%s, %s, %s, %s, %s)" % (exchanger, coin_symbol, transaction_time, operation, change))

    def get_exchanger(self):
        return self.__exchanger

    def get_coin_symbol(self):
        return self.__coin_symbol

    def get_transaction_time(self):
        return self.__transaction_time

    def get_operation(self):
        return self.__operation

    def get_change(self):
        return self.__change

    def get_event_number(self):
        return self.__event_nbr

    def get_gecko_object(self):
        return self.__gecko

    def get_note(self):
        return self.__note

    def set_note(self, note):
        if self.__note is None:
            self.__note = note
        else:
            self.__note = self.__note + note

    def print(self):
        print("event number: %s, coin: %s, price: %s, operation %s, change %s,  exchanger: %s, \
        transaction timestamp: %s, notes: %s" % (self.__event_nbr, self.__coin_symbol, self.__gecko.get_eur_price(),
                                                 self.__operation, self.__change, self.__exchanger,
                                                 self.__transaction_time, self.__note))
