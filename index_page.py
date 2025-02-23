from flask import Blueprint, render_template, request, jsonify
from sqlalchemy import func

from models import House

# 创建蓝图对象
index_page = Blueprint('index_page', __name__)

@index_page.route('/')
def index():
    house_total_unm = House.query.count()  # 获取房源总数
    house_new_list = House.query.order_by(House.publish_time.desc()).limit(6).all()  # 获取最新的6条房源数据
    house_hot_list = House.query.order_by(House.page_views.desc()).limit(4).all()  # 获取热门的4条房源数据
    return render_template('index.html', 
                           num = house_total_unm,
                           house_new_list = house_new_list,
                           house_hot_list = house_hot_list
                           )  # 渲染模板

@index_page.route('/search/keyword/', methods = ['POST'])
def search_kw():
    kw = request.form['kw']  # 获取搜索关键字
    info = request.form['info']  # 获取用户的搜索选项
    if info == '地区搜索':
        # 获取查询结果
        house_data = House.query.with_entities(
            House.address,
            func.count()
        ).filter(House.address.contains(kw))
        # 处理查询结果
        result = house_data.group_by('address').order_by(func.count().desc()).limit(9).all()
        if len(result):
            data = []
            for i in result:  # 有查询结果
                data.append({'t_name': i[0], 'num': i[1]})
            return jsonify({'code': 1, 'info': data})
        else:  # 无查询结果
            return jsonify({'code': 0, 'info': []})
    elif info == '户型搜索':
        house_data = House.query.with_entities(
            House.rooms, 
            func.count()
        ).filter(House.rooms.contains(kw))
        result = house_data.group_by('rooms').order_by(func.count().desc()).limit(9).all()
        if len(result):
            data = []
            for i in result:
                data.append({'t_name': i[0], 'num': i[1]})
            return jsonify({'code': 1, 'info': data})
        else:
            return jsonify({'code': 0, 'info': []})
    