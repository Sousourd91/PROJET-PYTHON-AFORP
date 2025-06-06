import random
import string

def generate_password():
    length = random.randint(12, 14)

    lowercase = ''.join(c for c in string.ascii_lowercase if c not in 'l')
    uppercase = ''.join(c for c in string.ascii_uppercase if c not in 'IO')
    digits = ''.join(c for c in string.digits if c not in '10')
    special_chars = '!@#$%^&*()-_=+[]{};:,.<>?'

    password = [
        random.choice(lowercase),
        random.choice(uppercase),
        random.choice(digits),
        random.choice(special_chars)
    ]

    all_chars = lowercase + uppercase + digits + special_chars

    password += random.choices(all_chars, k=length - len(password))

    random.shuffle(password)

    return ''.join(password)

print(generate_password())