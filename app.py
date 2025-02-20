from flask import Flask
from settings import Config

app = Flask(__name__)
app.config.from_object(Config)

@app.route('/')
def test():
    return 'Hello World!'

if __name__ == '__main__':
    app.run(debug=app.config['DEBUG'])