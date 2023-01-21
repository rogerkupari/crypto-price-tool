import xlsxwriter


class FileWriter:
    __logger = None
    __filePath = None
    __file = None
    __sheet = None
    __active_row = 0
    __active_column = 0
    __initialized = False

    def __init__(self, filePath):
        self.__filePath = filePath
        self.__file = xlsxwriter.Workbook(self.__filePath)
        self.__sheet = self.__file.add_worksheet("Transactions")

    def __del__(self):
        self.close_excel()

    def close_excel(self):
        self.__file.close()

    def next_line(self):
        self.__active_row += 1
        self.__active_column = 0

    def next_column(self):
        self.__active_column += 1

    def write_column(self, value):
        self.__sheet.write(self.__active_row, self.__active_column, value)
        self.next_column()

    def write_transactions_initial_line(self):
        self.write_column("Event n:o")
        self.write_column("Timestamp")
        self.write_column("Exchanger")
        self.write_column("Coin name")
        self.write_column("Operation")
        self.write_column("Change")
        self.write_column("EUR Price")
        self.write_column("Notes")
        self.next_line()
        self.__initialized = True

    def write_transaction(self, event, date, exchanger, coin, operation, change, price, notes):
        if not self.__initialized:
            self.write_transactions_initial_line()

        self.write_column(event)
        self.write_column(date)
        self.write_column(exchanger)
        self.write_column(coin)
        self.write_column(operation)
        self.write_column(change)
        self.write_column(price)
        self.write_column(notes)
        self.next_line()

    def write_coin_specific_initial_line(self):
        self.write_column("Event n:o")
        self.write_column("Timestamp")
        self.write_column("Coin name")
        self.write_column("Operation")
        self.write_column("Change")
        self.write_column("EUR Price")
        self.next_line()

    def add_coin_specific_sheet(self, name):
        self.__sheet = self.__file.add_worksheet(name)
        self.__active_row = 0
        self.__active_column = 0
        self.write_coin_specific_initial_line()

    def write_coin_specific_info(self, event, date, coin, operation, change, price):
        self.write_column(event)
        self.write_column(date)
        self.write_column(coin)
        self.write_column(operation)
        self.write_column(change)
        self.write_column(price)
        self.next_line()
