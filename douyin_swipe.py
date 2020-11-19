""" 抖音12.6版本滑动操作实现数据抓取"""
import time
import uiautomator2 as u2


class Douyin(object):
    # 在__init__方法里面连接设备
    def __init__(self):
        # u2连接设备的四种方式，connect_usb、connect_adb_wifi、connect_wifi、connect，注意携带的参数即可
        # 注意这里connect_adb_wifi方式，端口不能忘记
        # 模拟器用前三种方法连接不上时，使用u2.connect()连接
        # self.d = u2.connect_usb(serial=SJQNW18A31000337)
        # self.d = u2.connect_adb_wifi("192.168.3.3:5555")
        # self.d = u2.connect_wifi("192.168.3.3")
        self.d = u2.connect()
        # 启动app
        self.start_app()
        # 获取屏幕分辨率
        self.size = self.get_windowsize()
        # 启动监视器
        self.handle_watcher()
        # 是用来获取一个初始时间
        self.t0 = time.perf_counter()

    def start_app(self):
        """启动app"""
        self.d.app_start(package_name="com.ss.android.ugc.aweme")

    def stop_app(self):
        """app退出逻辑"""
        # 先关闭监视器
        self.d.watcher.stop()
        self.d.app_stop("com.ss.android.ugc.aweme")
        self.d.app_clear("com.ss.android.ugc.aweme")

    def stop_time(self):
        """停止时间"""
        # 时间是秒
        if time.perf_counter() - self.t0 > 300:
            return True

    # u2监视器，用来处理不定时弹出窗口的事件
    def handle_watcher(self):
        """监视器"""
        #位置信息授权
        self.d.watcher.when('//*[@resource-id="com.android.permissioncontroller:id/permission_allow_foreground_only_button"]').click()
        #获取设备信息授权
        self.d.watcher.when('//*[@resource-id="com.android.permissioncontroller:id/permission_allow_button"]').click()
        # 个人信息保护指引
        self.d.watcher.when('//*[@resource-id="com.ss.android.ugc.aweme:id/m7"]').click()
        # 滑动查看更多 //*[@text="滑动查看更多"]
        self.d.watcher.when('//*[@resource-id="com.ss.android.ugc.aweme:id/om"]').click()
        # 监控器写好之后，一定要记得启动
        self.d.watcher.start(interval=1)

    def get_windowsize(self):
        """获取窗口大小"""
        return self.d.window_size()

    def swipe_douyin(self):
        """滑动抖音视频和点击视频发布者头像的操作"""
        # 来判断是否正常的进入到了视频页面
        # 网络情况不好也包含在内了
        # 进入正常的视频页面,开始滑动
        if self.d(resourceId="com.ss.android.ugc.aweme:id/a05", text="消息").exists(timeout=20):
            # 添加循环，循环滑动和判断视频，实现持久化
            while True:
                # 设置停止循环的条件以及退出操作
                if self.stop_time():
                    self.stop_app()
                    return
                # 查看是不是正常的发布者
                if self.d(resourceId="com.ss.android.ugc.aweme:id/v7").exists :
                    time.sleep(1)
                    # 左滑进入发布者信息界面
                    self.d.swipe_ext("left")
                    # 判断当前页面是否拥有返回键
                    if self.d(resourceId="com.ss.android.ugc.aweme:id/et").exists:
                        time.sleep(3)
                        # 拥有返回键则右滑返回
                        self.d.swipe_ext("right")
                # 只要不是原创视频，不论广告还是什么一律上滑
                else:
                    if self.d(resourceId="com.ss.android.ugc.aweme:id/a05", text="消息").exists:
                        time.sleep(1)
                        # 上滑代码
                        x1 = int(self.size[0] * 0.5)
                        y1 = int(self.size[1] * 0.9)
                        y2 = int(self.size[1] * 0.15)
                        self.d.swipe(x1, y1, x1, y2)
                # 上述判断结束后进入当前判断，如果是发布者页面则进行上滑，如果不是则进行下次循环判断
                if self.d(resourceId="com.ss.android.ugc.aweme:id/a05", text="消息").exists and self.d(resourceId="com.ss.android.ugc.aweme:id/v7").exists:
                    time.sleep(1)
                    # 进入正常的视频页面,开始滑动
                    x1 = int(self.size[0] * 0.5)
                    y1 = int(self.size[1] * 0.9)
                    y2 = int(self.size[1] * 0.15)
                    self.d.swipe(x1, y1, x1, y2)


if __name__ == '__main__':
    # swipe_douyin方法退出APP后，循环启动APP，实现自动化持久化，无需再一次次手动的启动
    # u2有时候启动进程时可能失败，使用try，except，再次尝试即可
    while True:
        try:
            d = Douyin()
            d.swipe_douyin()
            time.sleep(3)
        except:
            continue

