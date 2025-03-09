from flask import Blueprint, render_template, jsonify
from sqlalchemy import func
from datetime import datetime, timedelta
import numpy as np
from sklearn.linear_model import LinearRegression

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

@detail_page.route('/get/piedata/<block>')
def return_pie_data(block):
    """获取指定区域的房源户型分布数据，返回json格式数据给前端"""
    result = House.query.with_entities(House.rooms, func.count()).filter(House.block == block).group_by(House.rooms).order_by(func.count().desc()).all()
    data = []   # 用于存放处理后的数据
    for i in result:
        data.append({'name': i[0], 'value': i[1]})
    return jsonify({'data': data})

@detail_page.route('/get/columndata/<block>')
def return_bar_data(block):
    """获取指定区域的房源数量TOP20，返回json格式数据给前端"""
    result = House.query.with_entities(House.address, func.count()).filter(House.block == block).group_by(House.address).order_by(func.count().desc()).all()
    name_list = []
    num_list = []
    for addr, num in result:
        residence_name = addr.rsplit('-', 1)[1]
        name_list.append(residence_name)
        num_list.append(num)
    if len(name_list) > 20:
        data = {'name_list_x': name_list[:20], 'num_list_y': num_list[:20]}
    else:
        data = {'name_list_x': name_list, 'num_list_y': num_list}
    return jsonify({'data': data})
    
@detail_page.route('/get/brokenlinedata/<block>')
def return_brokenline_data(block):
    """获取指定区域的房源价格走势数据，返回json格式数据给前端"""
    # 时间序列
    time_stamp = House.query.filter(House.block == block).with_entities(House.publish_time).all()
    time_stamp.sort(reverse=True)
    date_list = []
    for i in range(1,14):
        latest_release = datetime.fromtimestamp(int(time_stamp[0][0]))
        day = latest_release + timedelta(days=-i)
        date_list.append(day.strftime('%m-%d'))
    date_list.reverse()
    # 1室1厅的户型
    result = House.query.with_entities(func.avg(House.price / House.area)).filter(House.block == block, House.rooms == '1室1厅').group_by(House.publish_time).order_by(House.publish_time).all()
    data1 = []
    for i in result[-14:]:
        data1.append(round(i[0], 2))
    # 2室1厅的户型
    result = House.query.with_entities(func.avg(House.price / House.area)).filter(House.block == block, House.rooms == '2室1厅').group_by(House.publish_time).order_by(House.publish_time).all()
    data2 = []
    for i in result[-14:]:
        data2.append(round(i[0], 2))
    # 2室2厅的户型
    result = House.query.with_entities(func.avg(House.price / House.area)).filter(House.block == block, House.rooms == '2室2厅').group_by(House.publish_time).order_by(House.publish_time).all()
    data3 = []
    for i in result[-14:]:
        data3.append(round(i[0], 2))
    # 3室2厅的户型
    result = House.query.with_entities(func.avg(House.price / House.area)).filter(House.block == block, House.rooms == '3室2厅').group_by(House.publish_time).order_by(House.publish_time).all()
    data4 = []
    for i in result[-14:]:
        data4.append(round(i[0], 2))
    
    return jsonify({'data': {'1室1厅': data1, '2室1厅': data2, '2室2厅': data3, '3室2厅': data4, 'date_li': date_list}})

@detail_page.route('/get/scatterdata/<block>')
def return_scatter_data(block):
    """获取指定区域的房源面积价格散点图数据，返回json格式数据给前端"""
    # 获取时间序列
    result = House.query.with_entities(func.avg(House.price / House.area)).filter(House.block == block).group_by(House.publish_time).order_by(House.publish_time).all()
    time_stamp = House.query.filter(House.block == block).with_entities(House.publish_time).all()
    time_stamp.sort(reverse=True)
    date_list = []
    for i in range(1,30):
        latest_release = datetime.fromtimestamp(int(time_stamp[0][0]))
        day = latest_release + timedelta(days=-i)
        date_list.append(day.strftime('%m-%d'))
    date_list.reverse()
    # 获取平均价格
    data = []
    x = []
    y = []
    for index, i in enumerate(result):
        x.append([index])
        y.append(round(i[0], 2))
        data.append([index, round(i[0], 2)])
    # 对未来价格进行预测
    predict_value = len(data)
    predict_outcome = linear_model_main(x, y, predict_value)
    p_outcome = round(predict_outcome[0], 2)
    data.append([predict_value, p_outcome])
    return jsonify({'data': {'data-predict': data, 'date_li': date_list}})


# 辅助函数
def linear_model_main(X_parameters, Y_parameters, predict_value):
    """线性回归模型"""
    regr = LinearRegression()
    regr.fit(X_parameters, Y_parameters)
    predict_value = np.array([predict_value]).reshape(-1, 1)
    predict_outcome = regr.predict(predict_value)
    return predict_outcome


# 自定义过滤器
def deal_traffic_txt(word):
    """处理交通条件有无数据的情况"""
    if len(word) == 0 or word is None:
        return '暂无信息！'
    else:
        return word
detail_page.add_app_template_filter(deal_traffic_txt, 'dealNone')

