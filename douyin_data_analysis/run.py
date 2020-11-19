from flask import Flask, render_template, jsonify
from douyin_view import douyin_mysql

# 实例化flask
app = Flask(__name__)

# 注册路由
@app.route("/")
def index():
    return "Hello World"

@app.route("/get_echart_data")
def get_echart_data():
    info = {}
    # 今日点赞最多TOP5
    info['echart_1'] = douyin_mysql.query_today_dianzan_result()
    # 今日评论最多TOP5
    info['echart_2'] = douyin_mysql.query_today_video_result()
    # 每日抓取数量，折线图
    info['echart_4'] = douyin_mysql.query_job_result()
    # 今日发布作品最多TOP5
    info['echart_5'] = douyin_mysql.query_today_dianzan_result()
    # 所在国家最多TOP5
    info['echart_6'] = douyin_mysql.query_country_result()
    # 认证情况饼状图
    info['echart_31'] = douyin_mysql.query_verify_result()
    # 年龄
    info['echart_32'] = douyin_mysql.query_age_result()
    # 性别
    info['echart_33'] = douyin_mysql.query_gender_result()
    # 根据城市计数,全国人员使用分布热力图
    info['map'] = douyin_mysql.query_city_result()
    return jsonify(info)

@app.route("/douyin/",methods=['GET','POST'])
def douyin():
    # 库内数据总量，今日抓取量
    result = douyin_mysql.count_result()
    return render_template('index.html',result=result)



if __name__ == '__main__':
    # 启动flask方式一
    # from livereload import Server
    # server = Server(app.wsgi_app)
    # server.watch('**/*.*')
    # server.serve()

    # 启动flask方式二
    app.run(debug = True,host="0.0.0.0",port=80)
