import json
import re
import logging

'''Added a logger for easy traceback of errors'''

logger=logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

file_handler=logging.FileHandler("calculator.log")

formatter=logging.Formatter("%(asctime)s:%(name)s:%(levelname)s:%(message)s")
file_handler.setFormatter(formatter)

logger.addHandler(file_handler)

'''This method loads the language json corresponding to the language_code'''
def load_language(language_code):
    try:
        with open(f'lang/{language_code}.json', 'r', encoding='utf-8') as file:
            logger.info("Successfully found the language json file")
            return json.load(file)
    except FileNotFoundError:
        '''executes if the mentioned language_code is not found'''

        logger.warning("language file for {} cannot be found".format(language_code))
        print(f"Language file for {language_code} not found. Using default (en).")
        logger.info("Using the default language file (en)")

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
        logger.exception("User tried to divide by zero")

'''Calculates the value of the given expression'''
def calculate(expression):
    operators = {'+': add, '-': subtract, '*': multiply, '/': divide}

    elements = re.findall(r'(\d+\.?\d*)|([+\-*/])', expression)
    
    result = float(elements[0][0])

    for i in range(1, len(elements), 2):
    #moved the try except statements to avoid printing invalid expressions unnessarily
        try:
            operator = elements[i][1]
            operand = float(elements[i + 1][0])

            result = operators[operator](result, operand)
            logger.info("Successfully found the result")
        except (ValueError, ZeroDivisionError, KeyError,IndexError): 
            #IndexError happens when the user tries to enter something like 1#1 with no operands
            logger.exception("User tried to enter an invalid expression")
            return None


    return result

def main():
    language_code = input("Enter language code (cz, en, ru): ") #gets the language code from the user
    language = load_language(language_code) #calls the 'load_language' function with 'language_code' as parameter

    expression = input(language["enter_expression"]) #gets the expression from the user

    result = calculate(expression) #calls the 'calculate' function with 'expression' as parameter
    if result is not None:
        print(f"{language['result']} {result} 🎉") #prints the result
        logger.info("Successfully printed the result")
    else:
        print(f"{language['invalid_expression']} ❌") #prints invalid expression
        logger.error("Could not print result because user entered an invalid expression")

if __name__ == "__main__":
    main()