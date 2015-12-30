from flask import Flask


app = Flask(__name__)
app.debug = 1
app._logger = __debug__


@app.route('/')
def hello_world():
    return 'Hello World!'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9558)
