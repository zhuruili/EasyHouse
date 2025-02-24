from flask import Blueprint, render_template, request
import math

from models import House

# 创建蓝图对象
list_page = Blueprint('list_page', __name__)
@list_page.route('/query')
def search_info():
    # addr
    if request.args.get('addr'):
        addr = request.args.get('addr')
        result = House.query.filter(House.address == addr).order_by(House.publish_time.desc()).all()
        return render_template('search_list.html', house_list = result)
    # rooms
    if request.args.get('rooms'):
        rooms = request.args.get('rooms')
        result = House.query.filter(House.rooms == rooms).order_by(House.publish_time.desc()).all()
        return render_template('search_list.html', house_list = result)

@list_page.route('/list/pattern/<int:page>')
def return_new_list(page):
    house_num = House.query.count()  # 获取房源总数
    total_page = math.ceil(house_num / 10)  # 计算总页数
    result = House.query.order_by(House.publish_time.desc()).paginate(page=page, per_page=10)  # 分页查询
    return render_template('list.html', house_list = result.items, page_num = result.page, total_num = total_page)

@list_page.route('/list/hot_house/<int:page>')
def return_hot_list(page):
    house_num = House.query.count()
    total_page = math.ceil(house_num / 10)
    result = House.query.order_by(House.page_views.desc()).paginate(page=page, per_page=10)
    return render_template('list.html', house_list = result.items, page_num = result.page, total_num = total_page)

# 过滤器
def deal_title_over(word):
    """过滤器，处理过长的标题的，防止显示异常"""
    if len(word) > 15:
        return word[:15] + '...'
    else:
        return word

def deal_direction(word):
    """过滤器，处理部分朝向空值"""
    if word is None or len(word) == 0:
        return '暂无数据'
    else:
        return word
# 注册过滤器
list_page.add_app_template_filter(deal_title_over, 'dealover')
list_page.add_app_template_filter(deal_direction, 'dealdirection')