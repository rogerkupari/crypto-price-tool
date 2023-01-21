import os
import shutil
import pytest
import pandas
from file_writer import FileWriter


class TestFileWriter:

    __temp_folder = os.path.dirname(os.path.realpath(__file__)) + "/ut_temp"
    __temp_file = __temp_folder + "/" + "test_report.xlsx"
    __temp_file2 = __temp_folder + "/" + "test_report2.xlsx"
    __file_writer = None

    def setup_class(self):
        os.mkdir(self.__temp_folder)
        assert os.path.exists(self.__temp_folder)

    def teardown_class(self):
        shutil.rmtree(self.__temp_folder)
        assert not os.path.exists(self.__temp_folder)

    @pytest.mark.order(1)
    def test_write_file(self):
        topics = ["Event n:o", "Timestamp", "Exchanger", "Coin name", "Operation", "Change", "EUR Price", "Notes"]
        first_line = ["1", "1", "2", "3", "4", "5", "6", "7"]
        second_line = ["2", "7", "6", "5", "4", "3", "2", "1"]
        self.__file_writer = FileWriter(self.__temp_file)
        self.__file_writer.write_transaction("1", "1", "2", "3", "4", "5", "6", "7")
        self.__file_writer.write_transaction("2", "7", "6", "5", "4", "3", "2", "1")
        self.__file_writer = None
        assert os.path.exists(self.__temp_file)
        content = pandas.read_excel(self.__temp_file)
        for i in range(0, 8):
            assert content.columns[i] == topics[i]
            assert str(content[topics[i]][0]) == first_line[i]
            assert str(content[topics[i]][1]) == second_line[i]

    @pytest.mark.order(2)
    def test_new_sheet_write(self):
        topics = ["Event n:o", "Timestamp", "Coin name", "Operation", "Change", "EUR Price"]
        first_line = ["1", "1", "2", "3", "4", "5"]
        second_line = ["2", "5", "4", "3", "2", "1"]
        test_sheet_name = "TEST"
        sheet = FileWriter(self.__temp_file2)
        sheet.add_coin_specific_sheet(test_sheet_name)
        sheet.write_coin_specific_info("1", "1", "2", "3", "4", "5")
        sheet.write_coin_specific_info("2", "5", "4", "3", "2", "1")
        sheet = None
        assert os.path.exists(self.__temp_file2)
        content = pandas.read_excel(self.__temp_file2, sheet_name=test_sheet_name)
        for i in range(0, 5):
            assert content.columns[i] == topics[i]
            assert str(content[topics[i]][0]) == first_line[i]
            assert str(content[topics[i]][1]) == second_line[i]
