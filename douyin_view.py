import time
from sqlalchemy import func
from mitmdump_douyin_mysql import douyin_author,douyin_video
from mitmdump_douyin_mysql import Session


class HandleDouyinData(object):
    def __init__(self):
        # 实例化session信息
        self.mysql_session = Session()
        self.date = time.strftime("%Y-%m-%d",time.localtime())

    # 今日评论最多TOP5
    def query_commont_result(self):
        info = {}
        # 查询同一抖音ID今日发布作品的评论数，并取sum值
        result = self.mysql_session.query(douyin_video.douyin_id, douyin_video.nickname,
                 func.sum(douyin_video.comment_count)).filter(func.date_format(
                 douyin_video.video_upload_time, "%Y-%m-%d") == self.date).group_by(
                 douyin_video.douyin_id).order_by(func.sum(douyin_video.comment_count).desc()).limit(5).all()
        # print(result)
        data = [{"name":x[1],"value":x[2]} for x in result]
        name_list = [name['name'].replace(" ","")[0:4] for name in data]
        info['x_name'] = name_list
        info['data'] = data
        # print(info)
        return info

    # 今日发布作品最多TOP5------从视频表根据同一抖音ID的aweme_id字段使用count方法获取
    # 抖音昵称可以相同，防止昵称相同，group_by时用抖音ID
    def query_today_video_result(self):
        info = {}
        # 查询今日同一抖音ID发布作品的count值排序
        result = self.mysql_session.query(douyin_video.douyin_id,douyin_video.nickname,func.count(douyin_video.aweme_id)).filter(
            func.date_format(douyin_video.video_upload_time,"%Y-%m-%d") == self.date
        ).group_by(douyin_video.douyin_id).order_by(func.count(douyin_video.aweme_id).desc()).limit(5).all()
        # print(result)
        result_list3 = [{"name": x[1], "value": x[2]} for x in result]
        name_list = [name['name'].replace(" ","")[0:4] for name in result_list3]
        info['x_name'] = name_list
        info['data'] = result_list3
        # print(info)
        return info

    # 今日获赞最多TOP5------从视频表根据同一抖音ID的digg_count字段使用sum方法获取
    # 抖音昵称可以相同，防止昵称相同，group_by时用抖音ID
    def query_today_dianzan_result(self):
        info = {}
        # 查询今日同一抖音ID下的点赞值，并使用sum求和
        result = self.mysql_session.query(douyin_video.douyin_id,douyin_video.nickname, func.sum(douyin_video.digg_count)).filter(
            func.date_format(douyin_video.video_upload_time,"%Y-%m-%d") == self.date
        ).group_by(douyin_video.douyin_id).order_by(func.sum(douyin_video.digg_count).desc()).limit(5).all()
        # print(result)
        data = [{"name": x[1], "value": int(x[2])} for x in result]
        name_list = [name['name'].replace(" ", "")[0:4] for name in data]
        info['x_name'] = name_list
        info['data'] = data
        # print(info)
        return info

    # 所在国家最多Top4
    def query_country_result(self):
        info = {}
        result = self.mysql_session.query(douyin_author.country,func.count(douyin_author.country)).group_by(douyin_author.country).order_by(func.count(douyin_author.country).desc()).limit(4).all()
        # print(result)
        data = [{"name": x[0], "value": x[1]} for x in result]
        for i in data:
            if i['name'] == '暂未填写':
                i['name'] = '未填'
        name_list = [name['name'].replace(" ","") for name in data]
        info['x_name'] = name_list
        info['data'] = data
        # print(info)
        return info

    # 每日抓取数量，折线图
    def query_job_result(self):
        info = {}
        video_result = self.mysql_session.query(func.date_format(
            douyin_video.crawl_time, "%Y-%m-%d"),func.count(douyin_video.crawl_time)).group_by(
            func.date_format(douyin_video.crawl_time, "%Y-%m-%d")
        ).order_by(func.date_format(douyin_video.crawl_time, "%Y-%m-%d").desc()).limit(5).all()
        # print(video_result)
        author_result = self.mysql_session.query(func.date_format(
            douyin_author.crawl_time, "%Y-%m-%d"),func.count(douyin_author.crawl_time)).group_by(
            func.date_format(douyin_author.crawl_time, "%Y-%m-%d")
        ).order_by(func.date_format(douyin_author.crawl_time, "%Y-%m-%d").desc()).limit(5).all()
        # print(author_result)
        result1 = [{"name": x[0].split("-")[1]+"-"+x[0].split("-")[2], "value": x[1]} for x in video_result]
        result2 = [{"name": x[0].split("-")[1]+"-"+x[0].split("-")[2], "value": x[1]} for x in author_result]
        # print(result1)
        # print(result2)
        list_video = []
        n = len(result1)
        for i in range(1,len(result1)+1):
            list_video.append(result1[n-1])
            n-=1
        # print(list_video)
        list_author = []
        n = len(result1)
        for i in range(1, len(result2) + 1):
            list_author.append(result2[n - 1])
            n -= 1
        # print(list_author)
        name_list = [name['name'] for name in list_author]
        info['x_name'] = name_list
        info['video'] = list_video
        info['user'] = list_author
        # print(info)
        return info

    # 根据城市计数,全国人员使用分布热力图
    def query_city_result(self):
        info = {}
        # 查询每个的城市所拥有的人数
        result = self.mysql_session.query(douyin_author.city,func.count(douyin_author.city)).group_by(douyin_author.city).order_by(func.count(douyin_author.city).desc()).all()
        # print(result)
        # 排除掉未填写信息的
        result1 = [{"name": x[0], "value": x[1]} for x in result if x[0] !="暂未填写"]
        name_list = [name['name'] for name in result1]
        info['x_name'] = name_list
        info['data'] = result1
        # print(info)
        return info

    # 认证情况饼状图
    def query_verify_result(self):
        info = {}
        result = self.mysql_session.query(douyin_author.verify_type,func.count(douyin_author.verify_type)).group_by(douyin_author.verify_type).all()
        # print(result)
        data = [{"name": x[0], "value": x[1]} for x in result]
        name_list = [name['name'] for name in data]
        info['x_name'] = name_list
        info['data'] = data
        # print(info)
        return info

    # 年龄分布饼状图
    def query_age_result(self):
        info = {}
        result = self.mysql_session.query(douyin_author.age,func.count(
            douyin_author.age)).filter(douyin_author.age<101 ).filter(douyin_author.age>0).group_by(
            douyin_author.age).order_by(func.count(douyin_author.age).desc()).all()
        # print(result)
        data = [{'name':str(x[0])+'岁','value':x[1] }for x in result]
        name_list = [name['name'] for name in data[0:6]]
        info['x_name'] = name_list
        info['data'] = data
        # print(info)
        return info

    # 性别分布饼状图
    def query_gender_result(self):
        info = {}
        result = self.mysql_session.query(douyin_author.gender,func.count(douyin_author.gender)).group_by(douyin_author.gender).all()
        # print(result)
        data = [{"name": x[0], "value": x[1]} for x in result]
        name_list = [name['name'] for name in data]
        info['x_name'] = name_list
        info['data'] = data
        # print(info)
        return info

    # 抓取数量
    def count_result(self):
        info = {}
        video_count = self.mysql_session.query(douyin_video).count()
        author_count = self.mysql_session.query(douyin_author).count()
        info['all_count'] = int(video_count) + int(author_count)
        video_today = self.mysql_session.query(douyin_video.aweme_id).filter(func.date_format(douyin_video.crawl_time, "%Y-%m-%d")==self.date).count()
        # print(video_today)
        author_today = self.mysql_session.query(douyin_author.douyin_id).filter(func.date_format(douyin_author.crawl_time, "%Y-%m-%d")==self.date).count()
        # print(author_today)
        info['today_count'] = int(video_today) + int(author_today)
        # print(info)
        return info


douyin_mysql = HandleDouyinData()
if __name__ == '__main__':
    douyin_mysql.query_age_result()