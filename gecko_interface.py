import requests
import time
import logging
import logging.config
import configparser


class GeckoInterface:
    __url = "https://api.coingecko.com/api/v3/coins"
    __coin_list_url = __url + "/list?include_platform=false"
    __price_req_url = __url + "/%s/history?date=%s&localization=false"
    __sleep_time_seconds = 150
    __coin_list = None
    __logger = None

    def __init__(self):
        logging.config.fileConfig('conf/log.conf')
        self.__logger = logging.getLogger(type(self).__name__)

    def __check_response(self, response):
        if response.status_code == 200:
            return response.status_code
        elif response.status_code == 429:
            self.__logger.warning("Gecko rate limit exceeded, sleep %ss" % (self.__sleep_time_seconds))
            time.sleep(self.__sleep_time_seconds)
            return response.status_code
        else:
            return response.status_code

    def get_coin_list(self):
        self.__logger.debug("call")
        if not self.__coin_list:
            self.__logger.debug("HTTP request")
            resp = self.__request_coin_list()
            response_code = self.__check_response(resp)
            if response_code == 200:
                self.__coin_list = resp.json()
                return self.__coin_list
            elif response_code == 429:
                resp = self.__request_coin_list()
                if resp.status_code != 200:
                    self.__logger.error("Gecko coin list request failed err code: %d" % (resp.status_code))
                    return -1
                else:
                    self.__coin_list = resp.json()
                    return self.__coin_list
            else:
                self.__logger.error("Gecko coin list request failed err code: %d" % (resp.status_code))
                return -1

        else:
            self.__logger.debug("return list")
            return self.__coin_list

    def get_coin_price(self, date, coin_id):
        self.__logger.debug("args(%s,%s)" % (date, coin_id))
        resp = self.__request_coin_price(date, coin_id)
        response_code = self.__check_response(resp)
        if response_code == 200:
            return self.__parse_price_from_response(coin_id, resp)
        elif response_code == 429:
            resp = self.__request_coin_price(date, coin_id)
            if resp.status_code != 200:
                self.__logger.error("Gecko coin list request failed err code: %d" % (resp.status_code))
                return -1
            else:
                return self.__parse_price_from_response(coin_id, resp)
        else:
            self.__logger.error("Gecko coin price request failed err code: %d %s" % (resp.status_code, resp.json()['error']))
            return -1

    def get_coin_properties(self, coin_symbol):
        properties = []
        if self.__coin_list:
            for property in self.__coin_list:
                if property['symbol'].upper() == coin_symbol:
                    properties.append(property)
        else:
            list = self.get_coin_list()
            for property in list:
                if property['symbol'].upper() == coin_symbol:
                    properties.append(property)

        return properties

    def __request_coin_list(self):
        self.__logger.debug("url = %s: " % (self.__coin_list_url))
        resp = requests.get(self.__coin_list_url)
        return resp

    def __request_coin_price(self, date, coin_id):
        url = self.__price_req_url % (coin_id, date)
        self.__logger.debug("args(%s,%s) - url = %s: " % (date, coin_id, url))
        resp = requests.get(url)
        return resp

    def __parse_price_from_response(self, coin_id, response):
        try:
            return response.json()['market_data']['current_price']['eur']
        except Exception:
            self.__logger.error("Gecko coin price have not entry as ['market_data'] \
            ['current_price']['eur'] for %s" % (coin_id))
            return -1


class GeckoCoinConfig:
    __filename = 'conf/gecko_coin_item.conf'
    __config = configparser.ConfigParser()

    def __init__(self):
        self.__config.read(self.__filename)

    def has_coin(self, coin):
        return coin in self.__config

    def get_id(self, coin):
        return self.__config[coin]['id']

    def get_symbol(self, coin):
        return self.__config[coin]['symbol']

    def get_name(self, coin):
        return self.__config[coin]['name']


class GeckoItem:
    __api_id = None
    __name = None
    __symbol = None
    __date = None
    __eur_price = None
    __logger = None
    __config = GeckoCoinConfig()

    def __init__(self, date, symbol):
        logging.config.fileConfig('conf/log.conf')
        self.__logger = logging.getLogger(type(self).__name__)
        self.__date = date
        self.__symbol = symbol
        self.has_configuration(symbol)

    def set_item_properties(self, api_id, name):
        self.__api_id = api_id
        self.__name = name

    def get_id(self):
        return self.__api_id

    def get_name(self):
        return self.__name

    def get_symbol(self):
        return self.__symbol

    def get_date(self):
        return self.__date

    def has_configuration(self, symbol):
        if self.__config.has_coin(symbol):
            self.set_item_properties(self.__config.get_id(symbol), self.__config.get_name(symbol))
            return True
        else:
            self.__logger.warning("No configuration for symbol %s" % (symbol))
            return False

    def set_eur_price(self, price):
        if not self.__eur_price:
            self.__eur_price = price

    def get_eur_price(self):
        return self.__eur_price
