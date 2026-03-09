class PaymentMethod:
    def pay(self, gateway, amount):
        raise NotImplementedError()
    
class CashPayment(PaymentMethod):
    def pay(self, gateway, amount):
        return gateway.process_cash(amount)
    
class QRPayment(PaymentMethod):
    def __init__(self, qr_code):
        self.qr_code = qr_code

    def pay(self, gateway, amount):
        return gateway.process_qr(self.qr_code, amount)
    
class CreditCardPayment(PaymentMethod):
    def __init__(self, card_number, holder, expiry, cvv):
        exp_month, exp_year = expiry.split("/")

        self.card_number = card_number
        self.holder = holder
        self.exp_month = int(exp_month)
        self.exp_year = int(exp_year)

        if self.exp_year < 100:
            self.exp_year += 2000

        self.cvv = cvv


    def pay(self, gateway, amount):
        return gateway.process_credit_card(
            self.card_number,
            self.exp_month,
            self.exp_year,
            self.cvv,
            amount
        )