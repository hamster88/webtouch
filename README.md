# webtouch
Test the availability of web application program.

## Install
```shell
pip install git+https://github.com/hamster88/webtouch --force-reinstall
```

## Usage

```shell
webtouch URL [OPTIONS...]
```

### Options
- `-H <str>` Set headers. 
- `-c <int>` Maximum concurrency.
- `-d <float>` Submission delay between each requested task, setting it twice indicates the delay range.
- `-w <int>` Maximum count of watch (print request info)
- `-i <str>` Interpolation's rule.
- `--cookies <str>`  load cookies.txt
- `--hated <str>` Be hated trait.(TODO)
- `--retreat <str>` Do it after beging hated.(TODO)


### Interpolation
Insert dynamic data into the URL for each request.

**Example** 分别插入从1开始的递增数，5-10之间的随机数，毫秒精度的时间戳，随机8个字节的16进制数

```shell
webtouch 'http://example.com/query?id={}&name={}&time={}&key={}' \
    -i 1: -i 5-10 -i ms -i h8
```

**Rules**

```
Insert number: 
    X-Y   ramdom integer
    X:Y   cycle increment 

    X-  => X-2147483647
    Y   => 0-Y
    X:  => X:2147483647
    :Y  => 0:Y 

Insert timestamp: 
    ts   integer of seconds
    tm   decimal of seconds.millisecond
    ms   integer of millisecond

Insert string:  (TODO)
    sX-Y  ramdom length words and numbers
    wX-Y  ramdom length and words

Insert other:  (TODO)
    hN    random N bytes hex value
    uuid  uuid4() 8-4-4-4-12 format string
    A,B,C,...  random enumeration value

```

### Hated and retreat
预测被讨厌并采取措施

**Example:** 在收到429状态码、响应体小于1024字节或者内容包含`"captcha"`时, 休眠3分钟
```shell
webtouch 'http://example.com/' \
    --hated 429 \
    --hated size:1024 \
    --hated content:captcha \
    --retreat 180s
```




**hated:** 
检测什么情况是被讨厌了，条件均为or逻辑

```
N              响应状态码
size:N         响应体字节数小于N
content:TEXT   响应体文本解码后包含的内容
header:TEXT    响应头格式化后包含的内容
```


**retreat:** 
被讨厌后采取的措施

```
Ns    休眠 N 秒
exit  退出程序
```


## 模块设计

* `app` 入口模块, 处理用户输入, 定义如何启动程序, 如何显示内容
* `worker` 工作者模块，管理线程池， 负责被动接取并执行任务，完成的任务实例会缓存一定数量，用于后续统计分析
* `task` 任务单元模块, 定义任务类，实现业务逻辑

---

// 设计遇到一些困难
大概是这样的，app 启动一个子线程运行一个 worker 示例,
worker 管理一个线程池用于并行执行task， task

