class PlateTextFormatter:
    VALID_LETTERS = set("ABEKMHOPCTYX")
    VALID_DIGITS = set("0123456789")

    REPLACEMENTS = {
        "0": "O",
        "O": "0",
        "1": "Y",
        "Y": "1",
        "3": "E",
        "E": "3",
        "4": "A",
        "A": "4",
        "5": "S",
        "S": "5",
        "7": "T",
        "T": "7",
        "8": "B",
        "B": "8",
        "9": "P",
        "P": "9",
    }

    EXPECTED_PATTERN = [
        VALID_LETTERS,
        VALID_DIGITS,
        VALID_DIGITS,
        VALID_DIGITS,
        VALID_LETTERS,
        VALID_LETTERS,
    ]

    def format(self, text: str) -> str:
        cleaned = self._clean_and_uppercase(text)
        if len(cleaned) < 6:
            return "".join(cleaned)

        corrected = self._correct_characters(cleaned)
        formatted_text = self._apply_format(corrected)
        return formatted_text

    def _clean_and_uppercase(self, text: str) -> list[str]:
        text = text.replace(" ", "")
        return [c.upper() for c in text if self._is_valid_char(c)]

    def _is_valid_char(self, char: str) -> bool:
        upper_char = char.upper()
        return upper_char in self.VALID_LETTERS or char in self.VALID_DIGITS

    def _correct_characters(self, chars: list[str]) -> list[str]:
        corrected_chars = []
        expected_types = self._build_expected_pattern(len(chars))

        for i, char in enumerate(chars):
            if i >= len(expected_types):
                break

            expected = expected_types[i]
            if char in expected:
                corrected_chars.append(char)
            else:
                corrected_char = self.REPLACEMENTS.get(char, None)
                if corrected_char and corrected_char in expected:
                    corrected_chars.append(corrected_char)
                else:
                    corrected_chars.append("?")
        return corrected_chars

    def _build_expected_pattern(self, length: int) -> list[set[str]]:
        expected = self.EXPECTED_PATTERN[:]
        while len(expected) < length:
            expected.append(self.VALID_DIGITS)
        return expected

    def _apply_format(self, corrected: list[str]) -> str:
        base = "".join(corrected[:6])
        region = "".join(corrected[6:])[:3]
        return f"{base} {region}"
