def format_plate_text(text: str) -> str:
    valid_letters = set("ABEKMHOPCTYX")
    valid_digits = set("0123456789")

    replacements = {
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

    text = text.replace(" ", "")
    cleaned = [
        c.upper() for c in text if c.upper() in valid_letters or c in valid_digits
    ]

    if len(cleaned) < 6:
        return "".join(cleaned)

    expected_types = [
        valid_letters,
        valid_digits,
        valid_digits,
        valid_digits,
        valid_letters,
        valid_letters,
    ]

    for i in range(6, len(cleaned)):
        expected_types.append(valid_digits)

    corrected = []
    for i, char in enumerate(cleaned):
        if i >= len(expected_types):
            break

        expected = expected_types[i]
        if char in expected:
            corrected.append(char)
        else:
            corrected_char = replacements.get(char, None)
            if corrected_char and corrected_char in expected:
                corrected.append(corrected_char)
            else:
                corrected.append("?")

    corrected_text = "".join(corrected)

    base = corrected_text[:6]
    region = corrected_text[6:]
    formatted_text = base + " " + region[:3]
    return formatted_text
