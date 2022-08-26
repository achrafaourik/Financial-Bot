# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List
import requests
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
import json


def generate_token():
    test_user = {
        "email": "user@example.com",
        "password": "string",
        "name": "string"}
    requests.post('http://localhost:8000/api/user/create/', json=test_user)

    r = requests.post('http://localhost:8000/api/user/token/',
                          json={"email": "user@example.com",
                                "password": "string"})
    token = json.loads(r.text)['token']
    return token

# token = generate_token()

class ActionCreateAccountType(Action):

    token = generate_token()

    def name(self) -> Text:
        return "action_account_type"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        account_type = tracker.get_slot('account_type')
        if account_type == "savings":
            dispatcher.utter_message(text='print savings')
            data = {"account_type": "savings", "account_balance": 0}
            r = requests.post('http://localhost:8000/api/banking/accounts/', json=data, headers={'Authorization': 'Token ' + self.token})
            list_savings_accnts = json.loads(r.text)

        else:
            dispatcher.utter_message(text="print credit")

        return []
