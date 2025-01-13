from random import randint
from webmiss import FetchTask, wm
import requests

wm.concurrent  = 16

# 定义两个 URL 模板，用于模拟 API 请求
# 第一个 URL 用于获取令牌（token），需要提供用户名和密码
url1 = 'http://httpbin.org/uuid?action=get_token&username={}&password={}'
# 第二个 URL 用于模拟操作（例如点赞），需要提供帖子 ID 和令牌
url2 = 'http://httpbin.org/anything/post/{}?action=like&token={}'

# 定义一个自定义任务类 `CustomTask`，继承自 `FetchTask`
class CustomTask(FetchTask):
    # 定义属性，用于存储用户名、密码、令牌和帖子 ID
    username: str  # 用户名
    password: str  # 密码
    token: str     # 获取的令牌
    post_id: str   # 帖子 ID（任务 ID）

    # 初始化方法，用于创建任务对象并初始化相关属性
    def __init__(self):
        # 调用父类的初始化方法，会自动计数并分配id
        super().__init__()
        # 生成一些参数，格式化 URL1
        self.username = f'bot{randint(100, 995577)}'
        self.password = 'seceret'
        self.url = url1.format(self.username, self.password)

    # 定义任务的运行方法
    def run(self):
        # 发送 HTTP GET 请求到 URL1，用于获取令牌
        res = requests.get(self.url)
        
        #  从上一个请求结果获取下一个请求参数，格式化 URL2
        res.raise_for_status()
        payload = res.json()
        self.token = payload['uuid']
        self.post_id = str(self.tid)
        self.url = url2.format(self.post_id, self.token)

        # 发送 HTTP GET 请求到 URL2，用于执行后续操作
        res = requests.get(self.url)  
        # 验证操作成功
        res.raise_for_status()

#  触发任务的执行
# CustomTask.trigger()