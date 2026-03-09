import random
from datetime import datetime

class PaymentGateway:

    # ---------------- Luhn Algorithm ----------------

    def validate_card(self, card_number):
        digits = [int(d) for d in card_number]
        digits.reverse()

        total = 0

        for i, digit in enumerate(digits):
            if i % 2 == 1:
                digit *= 2
                if digit > 9:
                    digit -= 9
            total += digit

        return total % 10 == 0

    # ---------------- CREDIT CARD ----------------

    def process_credit_card(self, card_number, exp_month, exp_year, cvv, amount):
        if not self.validate_card(card_number):
            return False, "INVALID CARD NUMBER"

        if len(cvv) not in [3,4]:
            return False, "INVALID CVV"

        now = datetime.now()
        if exp_year < now.year or (exp_year == now.year and exp_month < now.month):
            return False, "CARD EXPIRED"

        if random.random() < 0.1:
            return False, "PAYMENT DECLINED"

        return True, "PAYMENT SUCCESS"

    # ---------------- QR ----------------

    def process_qr(self, qr_code, amount):
        if not qr_code:
            return False, "INVALID QR"

        return True, "QR PAYMENT SUCCESS"

    # ---------------- CASH ----------------

    def process_cash(self, amount):
        return True, "CASH RECEIVED"