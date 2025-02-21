from flask import Flask, render_template
from settings import Config

app = Flask(__name__, 
            static_folder='static',
            template_folder='templates')
app.config.from_object(Config)

@app.route('/')
def test():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=app.config['DEBUG'])