import random
import string

def generate_password(length=12, use_uppercase=True, use_lowercase=True, use_numbers=True, use_special=True):
    if length == 0:
        raise ValueError("Password length should be at least 1 character long.")
    
    character_pool = ""
    if use_uppercase:
        character_pool += string.ascii_uppercase
    if use_lowercase:
        character_pool += string.ascii_lowercase
    if use_numbers:
        character_pool += string.digits
    if use_special:
        character_pool += string.punctuation

    if not character_pool:
        raise ValueError("At least one character type must be selected.")
    
    # Ensure password includes at least one character from each selected category
    password = []
    if use_uppercase:
        password.append(random.choice(string.ascii_uppercase))
    if use_lowercase:
        password.append(random.choice(string.ascii_lowercase))
    if use_numbers:
        password.append(random.choice(string.digits))
    if use_special:
        password.append(random.choice(string.punctuation))
    
    # Fill the rest of the password length with random characters
    remaining_length = length - len(password)
    password.extend(random.choices(character_pool, k=remaining_length))
    
    # Shuffle the result to ensure randomness
    random.shuffle(password)
    
    return ''.join(password)


print(generate_password(length=16, use_uppercase=True, use_lowercase=True, use_numbers=True, use_special=True))