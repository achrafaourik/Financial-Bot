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
    time.sleep(60)  # wait for the django server to start before populating the db
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
            response = json.loads(r.text)

            dispatcher.utter_message(
                text='The {} account N° {} has been created properly.'.format(
                    account_type, response['id']))

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
            response = json.loads(r.text)

            print(type(response))

            for account in response:
                dispatcher.utter_message(
                    text="The {} account N° {}'s balance is : {}$.".format(
                    account['account_type'], account['id'], account['account_balance']))
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

            dispatcher.utter_message(text='Done!')

        else:
            dispatcher.utter_message(text='There is no such transaction type')

        return [SlotSet("transaction_type", None),
                SlotSet("amount-of-money", None),
                SlotSet("account_number", None)]


class ActionAskAccountNumber(Action):
    token = token

    def name(self) -> Text:
        return "action_ask_transaction_form_account_number"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        dispatcher.utter_message(text='On which account would you like to perform the transaction?')

        r = requests.get('http://localhost:9000/api/banking/accounts/',
                              headers={'Authorization': 'Token ' + self.token})
        response = json.loads(r.text)

        buttons = [{'payload': str(x['id']),
                    'title': x['account_type'].capitalize() + ' account N°: ' + str(x['id'])} for x in response]

        # buttons = [{'payload': '/make_transaction{{"account_number": "' + str(x['id']) + '"}}',
        #             'title': 'Account N°: ' + str(x['id'])} for x in response]

        dispatcher.utter_message(
            text='Here are the available accounts: ',
            buttons=buttons)

        return []
