import random, string

def generateAlphanumericKey():
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for i in range(8))