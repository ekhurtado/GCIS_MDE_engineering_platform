from flask import Flask, request

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def handle_message():
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
    else:
        return "Unsupported method"

if __name__ == '__main__':
    app.run()