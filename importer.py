import django
import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "transactions.settings")
django.setup()

import pandas as pd

FILE_PATH = "transactions.json"

MAX_DATE_DEVIATION = pd.Timedelta('3 days')
MIN_TRANSACTIONS_PER_SEQUENCE = 4
MIN_TRANSACTION_DATE_DIFF = pd.Timedelta('4 days')

from sequences.models import Transaction, Sequence


Transaction.objects.all().delete()


def get_description_key(string):
    """
    Transform the description to a unique description key
    """

    common_splitters = ["--", "*"]

    for spliter in common_splitters:
        if spliter in string:
            # if we have --, split the sting removing the last block of chars
            splited = string.split(spliter)
            return '_'.join(splited[:-1])

    if " " not in string:
        # if there are no spaces, no -- and no *, almost certain that's unique
        return string
    else:
        splited = string.split(" ")
        if not splited[-1].isalpha():
            return '_'.join(splited[:-1])
        else:
            return '_'.join(splited)


if __name__ == '__main__':

    df = pd.read_json(FILE_PATH)

    # creates groups of transactions based on the description
    df['group_key'] = df['description'].apply(get_description_key)

    groups = df.groupby('group_key')

    for group, transactions in groups:

        sequence_transactions = []
        # calculate the date diff for transactions
        transactions['diff'] = transactions['date'].diff().fillna(pd.Timedelta(seconds=0))
        # calculate the mean of the diff column
        mean = transactions['diff'].mean()

        for transaction in transactions.to_dict('records'):

            # Saves all transactions into the DB
            new_transaction = Transaction(date=transaction['date'],
                                          amount=transaction['amount'],
                                          description=transaction['description']
                                          )
            new_transaction.save()

            # Add transaction to a list if matches criteria
            if abs(transaction['diff'] - mean) < MAX_DATE_DEVIATION and mean > MIN_TRANSACTION_DATE_DIFF:
                sequence_transactions.append(new_transaction)

        # Create a sequence and save transactions into it, skip sequences smaller than 4 transactions
        if len(sequence_transactions) > MIN_TRANSACTIONS_PER_SEQUENCE:
            new_sequence = Sequence(name=group)
            new_sequence.save()
            new_sequence.transactions.add(*sequence_transactions)
