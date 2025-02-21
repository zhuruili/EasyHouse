from flask import Flask, render_template

from settings import Config, db
from models import House

app = Flask(__name__, 
            static_folder='static',
            template_folder='templates')
app.config.from_object(Config)
db.init_app(app=app)

@app.route('/')
def test():
    # 尝试查询数据库
    first_house = House.query.first()
    if first_house:
        print(first_house)
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=app.config['DEBUG'])