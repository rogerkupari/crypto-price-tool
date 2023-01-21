from binance_reader import BinanceReader


class TestBinanceReader:

    def test_incorrect_init(self):
        reader = BinanceReader(None)
        reader.Read()
        assert not reader.GetTransactions()

    def test_incorrect_file_init(self):
        reader = BinanceReader('test')
        # with pytest.raises(FileNotFoundError):
        reader.Read()
        assert not reader.GetTransactions()

    def test_init(self):
        reader = BinanceReader('ut/data_files/binance_test.csv')
        reader.Read()
        assert len(reader.GetTransactions()) == 11
