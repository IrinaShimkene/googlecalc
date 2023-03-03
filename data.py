import pytest
import random

def whole_numbers(num):
    text = '1234567890'
    rand_string = ''.join(random.choice(text) for i in range(num))
    return rand_string

def non_integer_numbers(num):
    rand_string = random.uniform(0, num)
    rand_string = str(rand_string)
    return rand_string

def whole_negative_numbers(num):
    text = '1234567890'
    rand_string = ''.join(random.choice(text) for i in range(num))
    rand_string = '-' + rand_string
    return rand_string