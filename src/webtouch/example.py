# 编写脚本来调用 webtouch
# 这里是在一个任务单元中执行多个相互依赖的http请求的例子

from random import randint
from webtouch import app, Task, FetchTask
import requests

# 设置app参数，这些可以被命令行参数覆盖
app.option.concurrent  = 16  # 并发数


# 第一个 URL 用于获取令牌（token），需要提供用户名和密码
url1 = 'http://httpbin.org/uuid?action=get_token&username={}&password={}'
# 第二个 URL 用于模拟操作（例如点赞），需要提供帖子 ID 和令牌
url2 = 'http://httpbin.org/anything/post/{}?action=like&token={}'

# 定义一个自定义任务类 `CustomTask`，继承自 `FetchTask`
class CustomTask(FetchTask):
    def __init__(self):
        # 调用父类的初始化方法，会自动计数并分配id
        super().__init__()
        
        # 生成一些参数
        self.username = f'bot{randint(100, 995577)}'
        self.password = 'seceret'
        self.password = 'seceret'
        self.token = '' # 后面的参数要从前一个请求中获取
        self.post_id = str(self.tid)
        
        # 设置父类的属性, 用于底层交互
        self.url = url1.format(self.username, self.password) # 先设置第一个 url
        self.title = f'Get token {self.username}'
        self.detail = f'get {self.url}'
        

    # 任务的入口方法
    def main(self):
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
        
        # 用 self.error 报告一些非预期情况
        # self.error = '429 Too Many Requests.'  
        # self.error = 'Invalid response data.'  

# 运行 app 
app.main(CustomTask)