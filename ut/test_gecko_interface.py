from gecko_interface import GeckoInterface, GeckoItem, GeckoCoinConfig
import pytest


class TestGeckoInterface:
    __gecko = GeckoInterface()

    def test_getters_gecko_interface(self):
        t = self.__gecko.get_coin_properties("BUSD")
        f = self.__gecko.get_coin_properties("_No_Exist")
        assert len(t) > 0
        assert len(f) == 0
        assert self.__gecko.get_coin_price("2022-11-11", "__TTEE") == -1
        assert self.__gecko.get_coin_price("2022-11-11", "busd") == -1

        for coin in range(50):
            assert self.__gecko.get_coin_price("11-11-2022", 'binance-usd') != -1


class TestGeckoCoinConfig:
    __cfg = GeckoCoinConfig()

    def test_has_coin(self):
        assert self.__cfg.has_coin('TEST') == True  # noqa: E712
        assert self.__cfg.has_coin('BTC') == False  # noqa: E712

    def test_getters(self):
        assert self.__cfg.get_id('TEST') == "test_api_key"
        assert self.__cfg.get_symbol('TEST') == "TEST"
        assert self.__cfg.get_name('TEST') == "test_coin_name"
        with pytest.raises(KeyError):
            assert self.__cfg.get_id('BTC') == "test_id"
            assert self.__cfg.get_symbol('BTC') == "test_symbol"
            assert self.__cfg.get_name('BTC') == "test_name"


class TestGeckoItem:
    __date = "2022-11-11"
    __symbol = "symbol"
    geckoItem = GeckoItem(__date, __symbol)

    def test_getters_after_init(self):
        assert self.geckoItem.get_id() == None  # noqa: E711
        assert self.geckoItem.get_name() == None  # noqa: E711
        assert self.geckoItem.get_symbol() == self.__symbol
        assert self.geckoItem.get_date() == self.__date

    def test_getters_after_set(self):
        coin_id = "test1"
        name = "test2"
        self.geckoItem.set_item_properties(coin_id, name)
        assert self.geckoItem.get_id() == coin_id
        assert self.geckoItem.get_name() == name
        assert self.geckoItem.get_symbol() == self.__symbol
        assert self.geckoItem.get_date() == self.__date
        assert self.geckoItem.has_configuration(self.__symbol) is False

    def test_get_and_set_eur_price(self):
        price = 1.234
        gecko = GeckoItem(self.__date, "BUSD")
        assert gecko.get_eur_price() is None
        gecko.set_eur_price(price)
        assert gecko.get_eur_price() == price
        gecko.set_eur_price(99.123)
        assert gecko.get_eur_price() == price
