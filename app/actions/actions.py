# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List
import requests
from rasa_sdk import Action, Tracker
from rasa_sdk.events import SlotSet
from rasa_sdk.executor import CollectingDispatcher
import json
import time


def create_user():
    time.sleep(60)
    test_user = {
        "email": "user@example.com",
        "password": "string",
        "name": "string"}
    requests.post('http://localhost:9000/api/user/create/', json=test_user)

def generate_token():
    create_user()

    r = requests.post('http://localhost:9000/api/user/token/',
                          json={"email": "user@example.com",
                                "password": "string"})
    token = json.loads(r.text)['token']
    return token

token = generate_token()


class ActionCreateAccountType(Action):
    token = token

    def name(self) -> Text:
        return "action_account_type"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        account_type = tracker.get_slot('account_type')
        if account_type in ["savings", 'credit']:
            dispatcher.utter_message(text='Creating a {} account...'.format(account_type))

            data = {"account_type": account_type, "account_balance": 0}
            r = requests.post('http://localhost:9000/api/banking/accounts/',
                              json=data,
                              headers={'Authorization': 'Token ' + self.token})
            response = str(json.loads(r.text))

            dispatcher.utter_message(text=response)
        else:
            dispatcher.utter_message(text='There is no such account type')

        return [SlotSet("account_type", None)]


class ActionCheckBalance(Action):
    token = token

    def name(self) -> Text:
        return "action_check_balance"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        account_type = tracker.get_slot('account_type')
        if account_type in ["savings", 'credit']:
            dispatcher.utter_message(
                text='Listing {} accounts balances..'.format(account_type))

            r = requests.get('http://localhost:9000/api/banking/accounts/?account_type=' + account_type,
                              headers={'Authorization': 'Token ' + self.token})
            response = str(json.loads(r.text))

            dispatcher.utter_message(text=response)
        else:
            dispatcher.utter_message(text='There is no such account type')

        return [SlotSet("account_type", None)]


class ActionMakeTransaction(Action):
    token = token

    def name(self) -> Text:
        return "action_make_transaction"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        transaction_amount = float(tracker.get_slot('amount-of-money'))
        account_number = tracker.get_slot('account_number')
        transaction_type = tracker.get_slot('transaction_type')

        if transaction_type in ["deposit", 'withdrawal']:
            dispatcher.utter_message(
                text='Performing a {} of {}$ on the account N°: {} ...'.format(
                    transaction_type,
                    transaction_amount,
                    account_number))

            data = {"account_type": account_number,
                    "transaction_type": transaction_type,
                    "transaction_amount": transaction_amount}


            r = requests.post('http://localhost:9000/api/banking/transactions/',
                              json=data,
                              headers={'Authorization': 'Token ' + self.token})
            response = str(json.loads(r.text))

            dispatcher.utter_message(text=response)

        else:
            dispatcher.utter_message(text='There is no such transaction type')

        return [SlotSet("transaction_type", None),
                SlotSet("amount-of-money", None),
                SlotSet("account_number", None)]
