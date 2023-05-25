import os, requests
from flask import Flask, request

function = os.environ.get('FUNCTION')
inPortNumber = os.environ.get('INPORT_NUMBER')
customization = os.environ.get('CUSTOMIZATION')

# TODO ezabatu
inPortNumber = 7000

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def main():
    print(request)

    # TODO MODIFIKATU
    if request.method == 'GET':
        # Handle GET requests
        return "Hello, GET request!"
    elif request.method == 'POST':
        # Handle POST requests
        print(request.data)
        for key, value in request.form.items():
            print("Key: {}, Value: {}".format(key, value))
        print("Full HTTP Message:")
        print("POST Request:")
        print("Headers: ", request.headers)
        print("Body: ", request.get_data(as_text=True))
        return "Hello, POST request"
    # ----------------------

    # TODO ezabatu
    function = "BalioaHanditu"

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
    app.run(port=inPortNumber)
