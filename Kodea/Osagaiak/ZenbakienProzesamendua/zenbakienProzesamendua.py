import os, requests

from flask import Flask, request

function = os.environ.get('function')
inPortNumber = os.environ.get('inPortNumber')
custom_step = os.environ.get('customization_urratsa')
custom_multiplier = os.environ.get('customization_biderkatzailea')

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
