import json
from typing import Optional
from argparse import ArgumentParser
import os


class FinanceDiary:
    def __init__(self, info_path, history_info_path):
        self.info_path = info_path
        self.history_info_path = history_info_path
        self.account_info = self.read_config()
        self.usd_balance = self.account_info['USD balance']
        self.sell_usd_course = self.account_info['sell dollar course']
        self.buy_usd_course = self.account_info['buy dollar course']
        # self.average_asset_value_usd = self.account_info["average asset value USD"]
        self.amount_spent_on_buying = self.account_info["amount spent on buying currency UA"]

    def read_config(self) -> dict:
        '''Метод который заранее вычитывает заготовленный файл и создает последующий файл истории'''
        if os.path.isfile(self.history_info_path) is False:
            with open(self.info_path, 'r') as file:
                dict_with_info = json.load(file)
        else:
            with open(self.history_info_path, 'r') as file:
                dict_with_info = json.load(file)
        return dict_with_info

    def rate_buy(self):
        '''Метод который выводит актуальный курс, по которому банк продает валюту'''
        print(f"1 USD / {self.buy_usd_course} UAH")

    def rate_sell(self):
        '''Метод который выводит актуальный курс, по которому банк покупает валюту'''
        print(f"1 USD / {self.sell_usd_course} UAH")

    def available(self):
        '''Метод который выводит сколько у пользователя накопленно валюты'''
        print(f"USD account balance: {self.usd_balance}")

    ###################################################################################################################
    # Методы которые выводит среднюю стоимость валюты -> сумма в гривнах потраченная на валюту / на кол-во валюты
    # Разбил на два метода, для того что бы в дальнейшем в методе использовать self.average_currency_val
    def average_currency_val(self) -> int:
        '''Методы которые выводит среднюю стоимость валюты -> сумма в гривнах потраченная на валюту / на кол-во валюты.
        Разбил на два метода, для того что бы в дальнейшем в методе использовать self.average_currency_val'''
        return self.amount_spent_on_buying / self.usd_balance

    def message_about_the_average_value(self):
        '''Методы которые выводит среднюю стоимость валюты -> сумма в гривнах потраченная на валюту / на кол-во валюты.
            Разбил на два метода, для того что бы в дальнейшем в методе использовать self.average_currency_val'''
        if self.amount_spent_on_buying == 0 and self.usd_balance == 0:
            print("We don't have any information of your balance")
        else:
            self.account_info["average asset value USD"] = self.average_currency_val()
            print(f"Your average currency USD {self.average_currency_val()}")
            return self.account_info

    ###################################################################################################################


    def buy(self, available: Optional[int] = 0) -> dict:
        '''Метод с помощью которого можно добавить USD'''
        need_uah = available * self.buy_usd_course
        self.account_info['amount spent on buying currency UA'] += round(need_uah, 2)
        self.account_info['USD balance'] += round(available, 2)
        return self.account_info

    def sell(self, available: Optional[int] = 0) -> dict:
        '''Метод с помощью которого можно "продать" USD'''
        if available > self.usd_balance:
            print(f"UNAVAILABLE, REQUIRED BALANCE USD {self.usd_balance}, AVAILABLE {available}")
        else:
            actual_usd: int = self.usd_balance - available
            actual_available_uah: int = available * self.average_currency_val()
            self.account_info['amount spent on buying currency UA'] -= round(actual_available_uah, 2)
            self.account_info['USD balance'] = round(actual_usd, 2)
        return self.account_info

    def restart(self):
        '''Метод с помощью которого можно удалить историю и данные'''
        os.remove(self.history_info_path)


def write_session_history(data):
    '''Метод который вносит изменения в историю trader_last_session.json'''
    with open("trader_last_session.json", 'w') as file:
        json.dump(data, file, indent=2)


args = ArgumentParser()
args.add_argument("CLI")
args.add_argument("SUM", type=str, nargs='?', default=0)
args = vars(args.parse_args())
amount = args["SUM"]
trader_account = FinanceDiary("config.json", "trader_last_session.json")
if args["CLI"] == "RATE_SELL":
    trader_account.rate_buy()
elif args["CLI"] == "RATE_BUY":
    trader_account.rate_sell()
elif args["CLI"] == "AVAILABLE":
    trader_account.available()
elif args["CLI"] == "AVERAGE_CURRENCY":
    write_session_history(trader_account.message_about_the_average_value())
elif args["CLI"] == "BUY" and args["SUM"]:
    write_session_history(trader_account.buy(int(amount)))
elif args["CLI"] == "SELL" and args["SUM"]:
    write_session_history(trader_account.sell(int(amount)))
elif args["CLI"] == "RESTART":
    trader_account.restart()
