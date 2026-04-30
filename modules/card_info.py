import re


class CardInfo:
    def __init__(self, card_number: str, card_type: str = "Visa", bank: str = "Sberbank"):
        self.card_type = card_type
        self.bank = bank
        self.raw_number = card_number
        self.normalized_number = self._normalize_number(card_number)
        self.formatted_number = self._format_number(self.normalized_number)

    def _normalize_number(self, number: str) -> str:
        digits = re.sub(r'\D', '', number)
        if len(digits) == 11:
            return digits
        elif len(digits) == 10:
            return '8' + digits
        return digits

    def _format_number(self, number: str) -> str:
        if len(number) >= 11:
            return f"+{number[0]} ({number[1:4]}) {number[4:7]}-{number[7:9]}-{number[9:11]}"
        return number

    def get_info(self) -> dict:
        return {
            "card_type": self.card_type,
            "bank": self.bank,
            "card_number": self.normalized_number,
            "formatted_card_number": self.formatted_number,
        }

    def display(self) -> None:
        print(f"\nCard Information:")
        print(f"   Type: {self.card_type}")
        print(f"   Bank: {self.bank}")
        print(f"   Number: {self.formatted_number}")
