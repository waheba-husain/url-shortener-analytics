# shortener.py
ALPHABET = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"

def encode(num: int) -> str:
    if num == 0:
        return ALPHABET[0]
    result = []
    while num > 0:
        remainder = num % 62
        result.append(ALPHABET[remainder])
        num //= 62
    return "".join(reversed(result))

def decode(short_code: str) -> int:
    result = 0
    length = len(short_code)
    for index, char in enumerate(short_code):
        position = ALPHABET.index(char)
        power = length - index - 1
        result += position * 62 ** power
    return result