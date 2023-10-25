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
        self.publicKey = None
        self.headers = None
        self.payerData = None


    """
        Method to set the appropriate payment keys
    """
    def setPaymentKeys(self, publicKey, accessToken, payerData):
        self.publicKey = publicKey
        self.headers = {
        'Authorization': f'Bearer {accessToken}',
        'Content-Type': 'application/json',
        }
        self.payerData = payerData

    def hasPaymentKeys(self):
        return not (self.publicKey == None or self.headers == None or self.payerData == None)

    """
        Method to create a qrcode for payment of specific amounts. It returs
    True or False depending on success of the request
    """
    def createPayment(self, amount, description):
        data = {
                "transaction_amount": amount,
                "description": description,
                "payment_method_id": self.method,
                "payer": self.payerData,
        }
        response = requests.post(PaymentManager.api_url, data=json.dumps(data), headers=self.headers)
        if response.status_code in [201, 200]:
            json_resp = response.json()
            resp = DotMap(json_resp)
            self.currentPayment = resp.id
            return True

        return False

    """
        Method to check if the last payment created is still valid
    """
    def checkPayment(self):
        if self.currentPayment == None:
            return None
        response = requests.get(PaymentManager.api_url + '/' + self.currentPayment, headers=self.headers)
        if response.status_code not in [201, 200]:
            return None
        json_resp = response.json()
        resp = DotMap(json_resp)
        return resp["status"]
