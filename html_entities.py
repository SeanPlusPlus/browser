# Dictionary mapping HTML entities to corresponding characters
entity_to_char = {
    "&nbsp;": " ", "&lt;": "<", "&gt;": ">", "&amp;": "&", "&quot;": '"', "&apos;": "'",
    "&plus;": "+", "&minus;": "-", "&times;": "×", "&divide;": "÷", "&equals;": "=", "&ne;": "≠", "&le;": "≤", "&ge;": "≥",
    "&dollar;": "$", "&euro;": "€", "&pound;": "£", "&yen;": "¥", "&cent;": "¢",
    "&copy;": "©", "&reg;": "®", "&trade;": "™", "&sect;": "§", "&para;": "¶", "&deg;": "°", "&micro;": "µ",
    "&larr;": "←", "&rarr;": "→", "&uarr;": "↑", "&darr;": "↓"
}

def replace_html_entities(input_string: str) -> str:
    for entity, char in entity_to_char.items():
        input_string = input_string.replace(entity, char)
    return input_string
