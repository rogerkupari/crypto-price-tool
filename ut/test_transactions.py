from transactions import Transaction
import datetime
from gecko_interface import GeckoCoinConfig


class TestTransaction:
    __event_nbr = 1
    __exchanger = "exchanger"
    __coin_symbol = "TEST"
    __transaction_time = "1980-10-11 12:13:14"
    __operation = "operation"
    __change = "change"
    __gecko_time = datetime.datetime.strptime(__transaction_time, '%Y-%m-%d %H:%M:%S').strftime('%d-%m-%Y')

    transaction = Transaction(__exchanger, __coin_symbol, __transaction_time, __operation, __change, __event_nbr)

    def test_getters_after_init(self):
        cfg = GeckoCoinConfig()
        assert self.transaction.get_exchanger() == self.__exchanger
        assert self.transaction.get_coin_symbol() == self.__coin_symbol
        assert self.transaction.get_transaction_time() == self.__transaction_time
        assert self.transaction.get_operation() == self.__operation
        assert self.transaction.get_change() == self.__change
        assert self.transaction.get_event_number() == self.__event_nbr
        assert self.transaction.get_gecko_object().get_date() == self.__gecko_time
        assert self.transaction.get_gecko_object().get_id() == cfg.get_id(self.__coin_symbol)
        assert self.transaction.get_gecko_object().get_name() == cfg.get_name(self.__coin_symbol)
        assert self.transaction.get_gecko_object().get_symbol() == cfg.get_symbol(self.__coin_symbol)

    def test_set_and_get_note(self):
        note = "Note. "
        secondNote = "Note2. "
        assert self.transaction.get_note() is None
        self.transaction.set_note(note)
        assert self.transaction.get_note() == note
        self.transaction.set_note(secondNote)
        assert self.transaction.get_note() == (note + secondNote)
