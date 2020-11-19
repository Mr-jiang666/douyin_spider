import json
import time

from sqlalchemy import create_engine, Integer,String,Text,DateTime
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column


'''
mitmdump+SQLAlchemy抓取抖音数据并存储到MySQL中
'''

# 创建数据库的连接，注意要先在数据库管理软件中创建好douyin_spider数据库
engine = create_engine("mysql://root:abc123456@127.0.0.1:3306/douyin_spider?charset=utf8mb4")
# 操作数据库，需要我们创建一个session
Session = sessionmaker(bind=engine)

# 声明一个基类
Base = declarative_base()


# douyin_video数据表，以及字段定义
class douyin_video(Base):
    # 表名称
    __tablename__ = 'douyin_video'
    # 视频ID
    aweme_id = Column(String(length=30),primary_key=True)
    # 作者抖音号
    douyin_id = Column(String(length=30), default="")
    # 作者昵称
    nickname = Column(String(length=20), default="")
    # 文案
    wenan = Column(Text, default="")
    # 点赞数
    digg_count = Column(Integer, default=0)
    # 评论数
    comment_count = Column(Integer, default=0)
    # 分享数
    share_count = Column(Integer, default=0)
    # 音乐标题
    music_title = Column(String(length=50), default="")
    # 音乐地址
    music_url = Column(String(length=200), default="")
    # 分享链接
    share_url = Column(String(length=200), default="")
    # 创建时间
    video_upload_time = Column(DateTime)
    # 抓取日期
    crawl_time = Column(DateTime)
    #更新时间
    update_time = Column(DateTime)


# douyin_author，以及字段定义
class douyin_author(Base):
    # 表名称
    __tablename__ = 'douyin_author'
    # 作者抖音号
    douyin_id = Column(String(length=30),primary_key=True)
    # 作者昵称
    nickname = Column(String(length=20), default="")
    # 认证类型
    verify_type = Column(String(length=6),default="未填写")
    # 认证信息
    verify_info = Column(String(length=20),default="未填写")#25
    # 性别
    gender = Column(String(length=8),default="未填写")
    # 国家
    country = Column(String(length=10),default="未填写")#20
    # 省份
    province = Column(String(length=10),default="未填写")
    # 城市
    city = Column(String(length=15),default="未填写")
    # 县区
    district = Column(String(length=20),default="未填写")
    # 学校
    school_name = Column(String(length=10),default="未填写")#20
    # 院系
    college_name = Column(String(length=10),default="未填写")#20
    # 生日
    birthday = Column(String(length=10),default="未填写")
    # 年龄
    age = Column(Integer,default=0)
    # 个性签名
    signature = Column(Text, default="")
    # 作品数量
    aweme_count = Column(Integer, default=0)
    # 较上次抓取新增作品数
    aweme_add = Column(Integer, default=0)
    # 总获赞数
    total_favorited = Column(Integer, default=0)
    # 较上次抓取新增点赞数
    dianzan_add = Column(Integer, default=0)
    # 关注数
    following_count = Column(Integer, default=0)
    # 较上次抓取新增关注数
    guanzhu_add = Column(Integer, default=0)
    # 粉丝数
    follower_count = Column(Integer, default=0)
    # 较上次抓取新增粉丝数
    fensi_add = Column(Integer, default=0)
    # 喜欢的作品数量
    favoriting_count = Column(Integer, default=0)
    # 较上次抓取新增喜欢作品数量
    xihuan_add = Column(Integer, default=0)
    # 抓取日期
    crawl_time = Column(DateTime)
    # 重置时间，每日00点重置新增的作品数、点赞数、关注数、粉丝数、喜欢数
    reset_time = Column(DateTime)
    #更新时间
    update_time = Column(DateTime)


# 新增数据和更新数据
class HandleDouyinData(object):
    def __init__(self):
        # 实例化session信息
        self.mysql_session = Session()

    # 数据的存储方法
    def insert_video(self,item):
        # 存储的数据结构
        data = douyin_video(
            # 视频ID
            aweme_id=item['aweme_id'],
            # 作者抖音号
            douyin_id=item['douyin_id'],
            # 作者昵称
            nickname=item['nickname'],
            # 文案
            wenan=item['wenan'],
            # 点赞数
            digg_count=item['digg_count'],
            # 评论数
            comment_count=item['comment_count'],
            # 分享数,
            share_count=item['share_count'],
            # 音乐标题
            music_title=item['music_title'],
            # 音乐地址
            music_url=item['music_url'],
            # 分享链接
            share_url=item['share_url'],
            # 创建时间
            video_upload_time=time.strftime("%Y--%m--%d %H:%M:%S", time.localtime(item['video_upload_time'])),
            # 抓取时间
            crawl_time=time.strftime("%Y--%m--%d %H:%M:%S", time.localtime(time.time())),
            # 更新时间
            update_time=time.strftime("%Y--%m--%d %H:%M:%S", time.localtime(time.time()))
        )
        query_result = self.mysql_session.query(douyin_video).filter(douyin_video.aweme_id==item['aweme_id']).first()
        if query_result:
            dict = {
            # 点赞数
            'digg_count' : item['digg_count'],
            # 评论数
            'comment_count' : item['comment_count'],
            # 分享数,
            'share_count' : item['share_count'],
            # 更新时间
            'update_time' : time.strftime("%Y--%m--%d %H:%M:%S", time.localtime(time.time()))
            }
            self.mysql_session.query(douyin_video).filter(
                douyin_video.aweme_id == item['aweme_id']).update(dict)
            # 提交数据到数据库
            self.mysql_session.commit()
            print("***********")
            print("***********")
            print("***********")
            print('更新一条短视频信息：%s：%s：%s' % (item['aweme_id'], item['douyin_id'], item['nickname']))
            print("***********")
            print("***********")
            print("***********")
        else:
            # 插入数据
            self.mysql_session.add(data)
            # 提交数据到数据库
            self.mysql_session.commit()
            print(">>>>>>>>>>")
            print(">>>>>>>>>>")
            print(">>>>>>>>>>")
            print('新增短视频信息：%s：%s：%s'%(item['aweme_id'],item['douyin_id'],item['nickname']))
            print(">>>>>>>>>>")
            print(">>>>>>>>>>")
            print(">>>>>>>>>>")

    # 数据的存储方法
    def insert_author(self,item):
        # 存储的数据结构
        data = douyin_author(
            # 作者抖音号
            douyin_id=item['douyin_id'],
            # 作者昵称
            nickname=item['nickname'],
            # 认证类型
            verify_type=item['verify_type'],
            # 认证信息
            verify_info=item['verify_info'],
            # 性别
            gender=item['gender'],
            # 国家
            country=item['country'],
            # 省份
            province=item['province'],
            # 城市
            city=item['city'],
            # 县区
            district=item['district'],
            # 学校
            school_name=item['school_name'],
            # 院系
            college_name=item['college_name'],
            # 生日
            birthday=item['birthday'],
            # 年龄
            age=item['age'],
            # 个性签名
            signature=item['signature'],
            # 作品数量
            aweme_count=item['aweme_count'],
            # 总获赞数
            total_favorited=item['total_favorited'],
            # 关注数
            following_count=item['following_count'],
            # 粉丝数,
            follower_count=item['follower_count'],
            # 喜欢的作品数量
            favoriting_count=item['favoriting_count'],
            # 抓取时间
            crawl_time=time.strftime("%Y--%m--%d %H:%M:%S", time.localtime(time.time())),
            # 抓取时间
            update_time=time.strftime("%Y--%m--%d %H:%M:%S", time.localtime(time.time()))
        )
        query_result = self.mysql_session.query(douyin_author).filter(douyin_author.douyin_id==item['douyin_id']).first()
        if query_result:
            # 较上次抓取新增作品数
            aweme = self.mysql_session.query(douyin_author.aweme_count).filter(douyin_author.douyin_id == item['douyin_id']).first()
            aweme_sql = self.mysql_session.query(douyin_author.aweme_add).filter(douyin_author.douyin_id == item['douyin_id']).first()
            aweme_add = int(item['aweme_count']) - int(aweme[0]) + int(aweme_sql[0])
            # 较上次抓取新增点赞数
            dianzan = self.mysql_session.query(douyin_author.total_favorited).filter(douyin_author.douyin_id == item['douyin_id']).first()
            dianzan_sql = self.mysql_session.query(douyin_author.dianzan_add).filter(douyin_author.douyin_id == item['douyin_id']).first()
            dianzan_add = int(item['total_favorited']) - int(dianzan[0]) + int(dianzan_sql[0])
            # 较上次抓取新增关注数
            guanzhu = self.mysql_session.query(douyin_author.following_count).filter(douyin_author.douyin_id == item['douyin_id']).first()
            guanzhu_sql = self.mysql_session.query(douyin_author.guanzhu_add).filter(douyin_author.douyin_id == item['douyin_id']).first()
            guanzhu_add = int(item['following_count']) - int(guanzhu[0]) + int(guanzhu_sql[0])
            # 较上次抓取新增粉丝数
            fensi = self.mysql_session.query(douyin_author.follower_count).filter(douyin_author.douyin_id == item['douyin_id']).first()
            fensi_sql = self.mysql_session.query(douyin_author.fensi_add).filter(douyin_author.douyin_id == item['douyin_id']).first()
            fensi_add = int(item['follower_count']) - int(fensi[0]) + int(fensi_sql[0])
            # 较上次抓取新增喜欢作品数量
            xihuan = self.mysql_session.query(douyin_author.favoriting_count).filter(douyin_author.douyin_id == item['douyin_id']).first()
            xihuan_sql = self.mysql_session.query(douyin_author.xihuan_add).filter(douyin_author.douyin_id == item['douyin_id']).first()
            xihuan_add = int(item['favoriting_count']) - int(xihuan[0]) + int(xihuan_sql[0])
            self.mysql_session.query(douyin_author).filter(
                douyin_author.douyin_id == item['douyin_id']).update({
                # 作品数量
                'aweme_count' : item['aweme_count'],
                # 总获赞数
                'total_favorited' :item['total_favorited'],
                # 关注数
                'following_count' : item['following_count'],
                # 粉丝数,
                'follower_count' : item['follower_count'],
                # 喜欢的作品数量
                'favoriting_count' : item['favoriting_count'],
                # 认证类型
                'verify_type' : item['verify_type'],
                # 认证信息
                'verify_info' : item['verify_info'],
                # 性别
                'gender' : item['gender'],
                # 国家
                'country' : item['country'],
                # 省份
                'province' : item['province'],
                # 城市
                'city' : item['city'],
                # 县区
                'district' : item['district'],
                # 学校
                'school_name' : item['school_name'],
                # 院系
                'college_name' : item['college_name'],
                # 生日
                'birthday' : item['birthday'],
                # 年龄
                'age' : item['age'],
                # 抓取时间
                'update_time' : time.strftime("%Y--%m--%d %H:%M:%S", time.localtime(time.time())),
                # 个性签名
                'signature' : item['signature'],
                'aweme_add': aweme_add,
                'dianzan_add': dianzan_add,
                'guanzhu_add': guanzhu_add,
                'fensi_add': fensi_add,
                'xihuan_add':xihuan_add
            })
            # 提交数据到数据库
            self.mysql_session.commit()
            print("***********")
            print("***********")
            print("***********")
            print('>>>>更新一条发布者信息：%s：%s' % (item['douyin_id'], item['nickname']))
            print("***********")
            print("***********")
            print("***********")
        else:
            # 插入数据
            self.mysql_session.add(data)
            # 提交数据到数据库
            self.mysql_session.commit()
            print(">>>>>>>>>>")
            print(">>>>>>>>>>")
            print(">>>>>>>>>>")
            print(">>>>>>>>>>")
            print('新增发布者信息：%s：%s'%(item['douyin_id'],item['nickname']))
            print(">>>>>>>>>>")
            print(">>>>>>>>>>")
            print(">>>>>>>>>>")


# 根据生日获取年龄
def get_age(birthday):
    str = birthday.split("-")[0]
    today = time.strftime("%Y-%m-%d", time.localtime())
    now_year = today.split("-")[0]
    age = int(now_year) - int(str)
    return age


def response(flow):
    # 使用mitmdump抓包视频页面，解析数据并进行抓取入库
    # 注意这里的url，不同版本App或者手机和模拟器之间都可能不同，抓取之前可以先用fiddler抓包确认一下url
    if 'https://aweme.snssdk.com/aweme/v1/feed' in flow.request.url:
        # 使用json来loadsresponse.text
        video_response = json.loads(flow.response.text)
        video_list = video_response.get("aweme_list", [])
        for item in video_list:
            data = {}
            # 视频ID
            if item.get("group_id",""):
                data['aweme_id'] = item.get("group_id","")
            else:
                data['aweme_id'] = item.get("aweme_id", "")
            if item.get("author", "").get("unique_id"):
                # 作者抖音号
                data['douyin_id'] = item.get("author", "").get("unique_id","")
            else:
                data['douyin_id'] = item.get("author", "").get("short_id", "")
            # 作者昵称
            data['nickname'] = item.get("author", "").get("nickname","")
            # 文案
            data['wenan'] = item.get("desc", "")
            # 点赞数
            data['digg_count'] = item.get("statistics","").get("digg_count", 0)
            # 评论数
            data['comment_count'] = item.get("statistics","").get("comment_count", 0)
            # 分享数
            data['share_count'] = item.get("statistics","").get("share_count", 0)
            # 创建时间
            data['video_upload_time'] = item.get("create_time","")
            # 音乐标题
            data['music_title'] = item.get("music", "").get("title", "")
            # 音乐地址
            data['music_url'] = item.get("music", "").get("play_url", "").get("uri", "")
            # 分享链接
            data['share_url'] = item.get("share_url", "")
            print(data)
            """写入Mysql数据库"""
            HandleDouyinData().insert_video(data)


    # 发布者页面信息抓取
    if 'https://aweme-eagle-lq.snssdk.com/aweme/v1/user/?user_id' in flow.request.url:
        person_response = json.loads(flow.response.text)
        person_info = person_response.get("user", "")
        if person_info:
            info = {}
            # 昵称
            info['nickname'] = person_info.get("nickname", "")
            if person_info.get("unique_id"):
                # 抖音号
                info['douyin_id'] = person_info.get("unique_id", "")
            else:
                info['douyin_id'] = person_info.get("short_id", "")
            if person_info.get("enterprise_verify_reason"):
                # 认证类型
                info['verify_type'] =  "官方账号认证"
                # 认证信息
                info['verify_info'] = person_info.get("enterprise_verify_reason", "")
            elif person_info.get("custom_verify"):
                # 认证类型
                info['verify_type'] = "个人账号认证"
                # 认证信息
                info['verify_info'] = person_info.get("custom_verify", "")
            else:
                # 认证类型
                info['verify_type'] = "未认证"
                # 认证信息
                info['verify_info'] = "未认证"
            # 性别
            if person_info.get("gender") == 0:
                info['gender'] = "未填写"
            elif person_info.get("gender") == 1:
                info['gender'] = "男"
            elif person_info.get("gender") == 2:
                info['gender'] = "女"
            else:
                info['gender'] = "请自行查询性别"
            # 国家
            if person_info.get("country") == "暂不设置":
                info['country'] = "暂未填写"
            elif person_info.get("country") == "":
                info['country'] = "暂未填写"
            else:
                info['country'] = person_info.get("country", "暂未填写")
            # 省份
            if person_info.get("province") == "":
                info['province'] = "暂未填写"
            else:
                info['province'] = person_info.get("province", "暂未填写")
            # 城市
            if person_info.get("city") == "":
                info['city'] = "暂未填写"
            else:
                info['city'] = person_info.get("city", "暂未填写")
            # 县区
            if person_info.get("district") == "":
                info['district'] = "暂未填写"
            else:
                info['district'] = person_info.get("district", "暂未填写")
            # 学校名称
            if person_info.get("school_name") == "":
                info['school_name'] = "暂未填写"
            else:
                info['school_name'] = person_info.get("school_name", "暂未填写")
            # 院系
            if person_info.get("college_name") == "":
                info['college_name'] = "暂未填写"
            else:
                info['college_name'] = person_info.get("college_name", "暂未填写")
            # 生日
            if person_info.get("birthday"):
                info['birthday'] = person_info.get("birthday", "")
                # 年龄
                info['age'] = get_age(info['birthday'])
            else:
                info['birthday'] = "暂未填写"
                info['age'] = 0
            # 个性签名
            info['signature'] = person_info.get("signature", "")
            # 作品数量
            info['aweme_count'] = person_info.get("aweme_count", 0)
            # 总获赞数
            info['total_favorited'] = person_info.get("total_favorited", 0)
            # 关注数
            info['following_count'] = person_info.get("following_count", 0)
            # 粉丝数
            info['follower_count'] = person_info.get("follower_count", 0)
            # 喜欢的作品数量
            info['favoriting_count'] = person_info.get("favoriting_count", 0)
            print(info)
            """写入Mysql数据库"""
            HandleDouyinData().insert_author(info)
