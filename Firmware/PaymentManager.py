import requests
import json
from pydotmap import DotMap
"""
Class that generates the appropriate payment through the MercadoPago api

Attributes
----------

api_url: static String
    http url to access the api

method: String
    string representing the payment method. always "pix"

payerData: dict
    dictionary with necessary personal information to generate payment. Needs keys email, first_name, last_name
and identification

currentPayment: String | None
    id of ongoing payment, stored as a string.

publicKey: String
    public key needed to acces MercadoPago api

headers: dict
    http header with the necessary information for every request. Contains the access token for autorization
and the type of the sent data (json)

"""
class PaymentManager:
    api_url = "https://api.mercadopago.com/v1/payments"
    def __init__(self):
        self.method = "pix"
        self.currentPayment = None
        self.headers = None


    """
        Method to set the appropriate payment keys
    """
    def setPaymentKeys(self, accessToken):
        self.headers = {
        'Authorization': f'Bearer {accessToken}',
        'Content-Type': 'application/json',
        }

    def hasPaymentKeys(self):
        return self.headers != None

    """
        Method to create a qrcode for payment of specific amounts. It returs
    True or False depending on success of the request
    """
    def createPayment(self, amount, description):
        from datetime import datetime, timedelta
        expiration = datetime.now() + timedelta(minutes=3)
        date_of_expiration = expiration.astimezone().isoformat(timespec='milliseconds')
        data = {
                "transaction_amount": amount,
                "description": description,
                "payment_method_id": self.method,
                "payer": {
                    "email": "customer@magehand.com",
                    "first_name": "MageHand",
                    "last_name": "Customer",
                    "identification": {
                        "type": "CPF",
                        "number": "01234567890",
                    },
                },
                "date_of_expiration": date_of_expiration
        }
        print(f'"date_of_expiration": {date_of_expiration}')
        response = requests.post(PaymentManager.api_url, data=json.dumps(data), headers=self.headers)
        if response.status_code in [201, 200]:
            json_resp = response.json()
            resp = DotMap(json_resp)
            self.currentPayment = resp.id
            return resp.point_of_interaction.transaction_data.qr_code_base64
        else:
            print(response.content)
            print(response.text)

        return False

    """
        Method to check if the last payment created is still valid
    """
    def checkPayment(self):
        if self.currentPayment == None:
            return None
        response = requests.get(PaymentManager.api_url + '/' + str(self.currentPayment), headers=self.headers)
        if response.status_code not in [201, 200]:
            return None
        json_resp = response.json()
        resp = DotMap(json_resp)
        return resp["status"]
