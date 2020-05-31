import requests
import json
from django.conf import settings


def verify_transaction(ref):
    url = 'https://api.paystack.co/transaction/verify/'+ref
    headers = {
        'Authorization': 'Bearer '+settings.PAYSTACK_SECRET_KEY,
        'Content-Type' : 'application/json',
        'Accept': 'application/json',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36',
        'cookie': 'J8JBNpPEVEjx3QA4zTpn'
    }
    x = requests.get(url, headers=headers)
    return x.json()
