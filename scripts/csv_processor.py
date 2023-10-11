import os
import scripts.utils

def parse_csv(csv_path, bank_type):

    #TODO: remove the need for an additional function just to call a function
    transactions = scripts.utils.read_csv(csv_path, bank_type)

    return transactions