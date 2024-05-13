import json
import re

def load_language(language_code):
    try:
        with open(f'lang/{language_code}.json', 'r', encoding='utf-8') as file:
            return json.load(file)
    except FileNotFoundError:
        print(f"Language file for {language_code} not found. Using default (en).")
        with open('lang/en.json', 'r', encoding='utf-8') as file:
            return json.load(file)

def add(x, y):
    return x + y

def subtract(x, y):
    return x - y

def multiply(x, y):
    return x * y

def divide(x, y):
    if y != 0:
        return x / y
    else:
        return "Cannot divide by zero"

def calculate(expression):
    operators = {'+': add, '-': subtract, '*': multiply, '/': divide}

    elements = re.findall(r'(\d+\.?\d*)|([+\-*/])', expression)
    
    result = float(elements[0][0])

    for i in range(1, len(elements), 2):
        operator = elements[i][1]
        operand = float(elements[i + 1][0])

        result = operators[operator](result, operand)

    return result

def main():
    language_code = input("Enter language code (cz, en, ru): ")
    language = load_language(language_code)

    expression = input(language["enter_expression"])

    try:
        result = calculate(expression)
        print(f"{language['result']} {result} 🎉")
    except (ValueError, ZeroDivisionError, KeyError):
        print(f"{language['invalid_expression']} ❌")

if __name__ == "__main__":
    main()