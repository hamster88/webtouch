from random import randint
import time
import requests
from webtouch import user_agents
from webtouch import util


LOW_DEFAULT_HEADERS = {
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "accept-encoding": "gzip, deflate, br, zstd",
        "accept-language": "zh-CN,zh;q=0.9",
        "cache-control": "max-age=0",
        "priority": "u=0, i",
        "sec-fetch-dest": "document",
        "sec-fetch-mode": "navigate",
        "sec-fetch-site": "none",
        "sec-fetch-user": "?1",
        "upgrade-insecure-requests": "1",
        "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 14.0) AppleWebKit/618.23.1 (KHTML, like Gecko) Version/17.3 Safari/618.23.1"
}

DEFAULT_HEADERS={
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,/;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "Accept-Encoding": "gzip, deflate, br, zstd",
    "Accept-Language": "zh-CN,zh;q=0.9",
    "Cache-Control": "max-age=0",
    "Priority": "u=0, i",
    "Sec-Fetch-Dest": "document",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-Site": "none",
    "Sec-Fetch-User": "?1",
    "Upgrade-Insecure-Requests": "1",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 14.0) AppleWebKit/618.23.1 (KHTML, like Gecko) Version/17.3 Safari/618.23.1"
}

class Fetch:
    '''
    封装 requests.get 
    '''
    res: requests.Response
    url: str
    phase: str  # ready, active, end
    start_time: float
    end_time: float
    error: Exception
    headers = DEFAULT_HEADERS
    cookie_jar = None
    id:str = 'noid'
    _len:int = 0

    def __init__(self, url, note=None, cookie_jar=None, ua=None, new_headers=None):
        '''
        初始化 Fetch 类实例
        :param url: 请求的 URL
        :param note: 用于标注请求的备注
        '''
        self.url = url
        self.note = note or url  # 如果没有备注，则默认使用 URL
        self.phase = 'ready'  # 初始状态为 ready
        self.start_time = 0
        self.end_time = 0
        self.error = None
        self.res = None

        self.cookie_jar = cookie_jar
        
        #randomized X-Forwarded-For and X-Real-IP address
        self.headers['X-Forwarded-For'] = randip()
        self.headers['X-Real-IP'] = randip()

        if ua:
            self.headers['User-Agent'] = ua
        else:
            self.headers['User-Agent'] = randua()
            
        if new_headers:
            self.headers.update(new_headers)



    def run(self):
        '''
        发起 GET 请求
        '''
        self.start_time = time.time()  # 记录请求开始时间
        self.phase = 'active'  # 更新状态为 active
 
        try:
            self.res = requests.get(self.url,
                    cookies=self.cookie_jar,
                    allow_redirects=True, 
                    headers=self.headers)  
        except Exception as e:
            self.error = e  # 捕获异常信息
        finally:
            self.end_time = time.time()  # 记录请求结束时间
            self.phase = 'end'  # 无论成功与否，状态都更新为 end


    def elapsed_time(self) -> float:
        '''
        计算请求耗时
        :return: 请求耗时（秒）
        '''
        if self.phase == 'end':  # 只有请求结束后才计算耗时
            return self.end_time - self.start_time
        
        if self.phase == 'active':
            # 如果请求未结束，返回当前已经经过的时间
            return time.time() - self.start_time if self.start_time else None
        
        return 0

    def report(self) -> str:
        '''
        生成请求的简略报告
        :return: 包括状态码、耗时和 Content-Length 的报告字符串
        '''
        if self.phase != 'end':  # 如果请求未结束，返回提示
            return 'Request is not completed yet.'
        
        elapsed = self.elapsed_time()

        if self.error:  # 如果请求出错，返回错误信息
            return f'Fail  {int(elapsed)}s  {self.url}  {self.error}'
        
        status  = self.res.status_code if self.res != None else '---'
        length = self.res.headers.get('Content-Length', 0) 
        
        if length == 0:
            try:
               length = len(self.res.content)
            except TypeError:
                pass
            
        self._len = int(length)
        return f' {status}  {elapsed:.2f}s  {util.gmkb(length)}'
    
    
    def see(self):
        if self.phase == 'ready':
            return f'Ready {self.note}'
        if self.phase == 'end':
            return self.report()
        
        elapsed = self.elapsed_time()
        n = int(elapsed)
        look_cookie = self.cookie_jar and f'(cookies:{len(self.cookie_jar)})' or ''
        return f'{n:>3}s  {self.note}    ' + look_cookie


    
    def __str__(self):
        '''
        格式化类的输出信息
        '''
        n = int(self.elapsed_time())
        return f'[{self.phase}]\t{n}\t{self.note} '
    
    def __len__(self):
        return len(self._len)

def randip():
    b = []
    for i in range(4):
        b.append(str(randint(1,255)))
    return '.'.join(b)

def randua():
    uas = user_agents.db
    i = randint(0,len(uas))
    return uas[i]['userAgent']
    
    
