import os, requests
from flask import Flask, request

function = os.environ.get('FUNCTION')
inPortNumber = os.environ.get('INPORTNUMBER')
customization = os.environ.get('CUSTOMIZATION')

app = Flask(__name__)

@app.route('/')
def main():
    print(request)
    match function:
        case "BalioaHanditu":
            increaseValue()
        case "BalioaTxikitu":
            decreaseValue()
        case "BalioaBiderkatu":
            multiplyValue()
        case _:
            return "Not function selected"


'''
Funtzionalitateak exekutatzeko metodoak
'''


def increaseValue():
    pass


def decreaseValue():
    pass


def multiplyValue():
    pass


if __name__ == '__main__':
    app.run()
