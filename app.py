from flask import Flask, render_template

from settings import Config, db
from models import House
from index_page import index_page
from list_page import list_page

app = Flask(__name__, 
            static_folder='static',
            template_folder='templates')
app.config.from_object(Config)
db.init_app(app=app)

app.register_blueprint(index_page, url_prefix='/')  # 注册蓝图`index_page`
app.register_blueprint(list_page, url_prefix = '/')  # 注册蓝图`list_page`

if __name__ == '__main__':
    app.run(debug=app.config['DEBUG'])