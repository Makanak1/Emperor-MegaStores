from django.conf import settings
import requests


class Paystack:
    PAYSTACK_SECRET_KEY = settings.PAYSTACK_SECRET_KEY
    base_url = "https://api.paystack.co"

    def verify_payment(self, reference, amount):  # Fix: removed invalid *args — only reference and amount needed
        path = f"/transaction/verify/{reference}"  # Fix: missing leading slash caused malformed URL
        headers = {
            "Authorization": f"Bearer {self.PAYSTACK_SECRET_KEY}",
            "Content-Type": "application/json"
        }
        url = self.base_url + path
        response = requests.get(url, headers=headers)

        # Fix: original returned response.json() immediately, making all code below unreachable
        if response.status_code == 200:
            response_data = response.json()
            if 'data' in response_data:
                return response_data['status'], response_data['data']
            else:
                return False, response_data.get('message', 'Payment verification failed')
        else:
            return False, response.json().get('message', 'Payment verification failed')