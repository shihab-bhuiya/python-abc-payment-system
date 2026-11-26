
from abc import ABC, abstractmethod


class PaymentInterface(ABC):

    @abstractmethod
    def process_payment(
        self,
        amount: float,
        currency: str
    ) -> bool:
        pass


class BkashPayment(PaymentInterface):

    def process_payment(
        self,
        amount: float,
        currency: str
    ) -> bool:

        if amount <= 0 or not currency:
            return False

        print("bKash Payment Information")
        print(f"Amount: {amount}")
        print(f"Currency: {currency}")
        print("Payment Method: Mobile Banking")

        return True


class CardPayment(PaymentInterface):

    def process_payment(
        self,
        amount: float,
        currency: str
    ) -> bool:

        if amount <= 0 or not currency:
            return False

        print("Card Payment Information")
        print(f"Amount: {amount}")
        print(f"Currency: {currency}")
        print("Payment Method: Debit/Credit Card")

        return True


class NagadPayment(PaymentInterface):

    def process_payment(
        self,
        amount: float,
        currency: str
    ) -> bool:

        if amount <= 0 or not currency:
            return False

        print("Nagad Payment Information")
        print(f"Amount: {amount}")
        print(f"Currency: {currency}")
        print("Payment Method: Mobile Financial Service")

        return True


# Creating objects
bkash = BkashPayment()
card = CardPayment()
nagad = NagadPayment()


# Processing payments
print(bkash.process_payment(1500, "BDT"))
print(card.process_payment(2500, "BDT"))
print(nagad.process_payment(1000, "BDT"))
