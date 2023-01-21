from transactions import Transaction
import csv
import logging
import logging.config


class BinanceReader:
    __file = None
    __transactions = []
    __logger = None

    def __init__(self, file):
        self.__file = file
        logging.config.fileConfig('conf/log.conf')
        self.__logger = logging.getLogger(type(self).__name__)

    def Read(self):
        try:
            event = 0
            with open(self.__file, newline='') as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    binance_time = row['UTC_Time']
                    binance_symbol = row['Coin']
                    change_count = row['Change']
                    coin_operation = row['Operation']
                    event += 1
                    self.__transactions.append(Transaction("binance", binance_symbol,
                                                           binance_time, coin_operation, change_count, event))
                    # print(row['UTC_Time'], row['Coin'], row['Change'])
                    # print(coin_gecko_time)
        except Exception as e:
            self.__logger.error("Cannot read file %s, msg=%s" % (self.__file, e))

    def GetTransactions(self):
        return self.__transactions
