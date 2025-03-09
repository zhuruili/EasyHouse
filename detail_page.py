from flask import Blueprint, render_template

from models import House

detail_page = Blueprint('detail_page', __name__)

@detail_page.route('/house/<int:house_id>')
def detail(house_id):
    # 查询房源id为`house_id`的房源信息
    house = House.query.get(house_id)
    # 获取房源对象的配套设施信息，形如：床-宽带-洗衣机-空调-热水器
    facilities_str = house.facilities
    # 将配套设施信息转换为列表
    facilities_list = facilities_str.split('-')

    return render_template('detail_page.html', house=house, facilities=facilities_list)


# 自定义过滤器
def deal_traffic_txt(word):
    """处理交通条件有无数据的情况"""
    if len(word) == 0 or word is None:
        return '暂无信息！'
    else:
        return word
detail_page.add_app_template_filter(deal_traffic_txt, 'dealNone')

