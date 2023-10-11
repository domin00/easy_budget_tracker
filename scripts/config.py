import os
import json

def check_bank_support(bank_type):

    with open('data/supported_banks.json', 'r') as file:
        supported_banks = json.load(file)

        if bank_type in supported_banks:
            return 

