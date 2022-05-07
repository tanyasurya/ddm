import random

def passgen(event, context):
    chars = event['chars']
    allowed_characters = "abcdefghijklmnopqrstuvwxyz01234567890ABCDEFGHIJKLMNOPQRSTUVWXYZ!@#$%^&*()?"
    generated = random.sample(allowed_characters, chars)
    return "".join(generated)

