# webtouch
Test the availability of web services

## Install
```shell
pip install git+https://github.com/hamster88/webtouch --force-reinstall
```

## Usage

```shell
webtouch URL  [-c CONCURRENT] [-d DELAY] [-w WATCH] [-i INTERPOLATION]
```

### Options
- `-c <int>` Maximum concurrency.
- `-d <float>` Submission delay between each requested task, setting it twice indicates the delay range.
- 
