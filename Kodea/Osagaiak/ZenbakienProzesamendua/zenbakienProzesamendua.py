import os, requests

function = os.environ.get('function')
inPortNumber = os.environ.get('inPortNumber')
custom_step = os.environ.get('customization_urratsa')
custom_multiplier = os.environ.get('customization_biderkatzailea')

def main():
    match function:
        case "BalioaHanditu":
            increaseValue()
        case "BalioaTxikitu":
            decreaseValue()
        case "BalioaBiderkatu":
            multiplyValue()
        case _:
            pass