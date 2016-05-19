from flask import Flask

# simple webserver for the sake of a localhost callback

app = Flask('__name__')

PORT = 8080

@app.route("/")
def index():
    return 'hello world'

@app.route("/callback")
def callback():
    return 'got the goods'

if __name__ == "__main__":
    app.run(debug=True, port=PORT)
