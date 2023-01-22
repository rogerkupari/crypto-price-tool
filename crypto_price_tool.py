import argparse
from binance_reader import BinanceReader
from gecko_interface import GeckoInterface, GeckoCoinConfig
from file_writer import FileWriter
import logging

logging.config.fileConfig('conf/log.conf')
__logger = logging.getLogger(__name__)


def get_differ_symbols_from_transactions(transactions):
    symbols = []
    for transaction in transactions:
        symbol = transaction.get_coin_symbol()
        if symbol not in symbols:
            symbols.append(symbol)

    return symbols


def check_symbol_configurations(transactions, connector):
    findings = False
    cfg = GeckoCoinConfig()
    for symbol in get_differ_symbols_from_transactions(transactions):
        if (not cfg.has_coin(symbol) and symbol != 'EUR'):
            findings = True
            properties = connector.get_coin_properties(symbol)
            print("Add configuration for %s:" % (symbol))
            for item in properties:
                print("%d) option: \n \
                [%s]\n \
                id = %s \n \
                name = %s \n \
                symbol = %s \n" % (properties.index(item), symbol, item['id'], item['name'], item['symbol']))

    return findings


def attach_eur_prices_to_coins(transactions, connector):
    for transaction in transactions:
        symbol = transaction.get_coin_symbol()
        if symbol != 'EUR':
            cfg = GeckoCoinConfig()
            id = cfg.get_id(symbol)
            date = transaction.get_gecko_object().get_date()
            price = connector.get_coin_price(date, id)
            if price == -1:
                price = connector.get_coin_price(date, id)
                if price == -1:
                    transaction.set_note("Price not available")
                    # raise RuntimeError("Unable to get coin price for id %s" % (id))
                    __logger.error("Unable to get coin price for id %s" % (id))
            transaction.get_gecko_object().set_eur_price(price)
        else:
            transaction.get_gecko_object().set_eur_price(1.0)


parser = argparse.ArgumentParser()
parser.add_argument('--binance', type=str, help="Path to the binance csv report", required=True)
parser.add_argument('--output', type=str, help="Path to output .xlsx report", required=True)
args = parser.parse_args()

reportPath = args.binance
reader = BinanceReader(reportPath)
reader.Read()
transactions = reader.GetTransactions()

connector = GeckoInterface()

if check_symbol_configurations(transactions, connector):
    print("Set coin configurations and try again")
    exit(0)

attach_eur_prices_to_coins(transactions, connector)

report = FileWriter(args.output)

for transaction in transactions:
    # transaction.print()
    report.write_transaction(transaction.get_event_number(),
                             transaction.get_transaction_time(),
                             transaction.get_exchanger(),
                             transaction.get_coin_symbol(),
                             transaction.get_operation(),
                             transaction.get_change(),
                             transaction.get_gecko_object().get_eur_price(),
                             transaction.get_note())

symbols = get_differ_symbols_from_transactions(transactions)

for symbol in symbols:
    report.add_coin_specific_sheet(symbol)
    for transaction in transactions:
        if symbol == transaction.get_coin_symbol():
            report.write_coin_specific_info(transaction.get_event_number(),
                                            transaction.get_transaction_time(),
                                            transaction.get_coin_symbol(),
                                            transaction.get_operation(),
                                            transaction.get_change(),
                                            transaction.get_gecko_object().get_eur_price())
