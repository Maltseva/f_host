# **Simple async file hosting**


![main window](img/main.png?raw=true)


## Description

Asynchronous file hosting on Python. Just for fun. 


![](https://img.shields.io/badge/Platform-windows%20%7C%20os--x%20%7C%20linux-orange)
![](https://img.shields.io/badge/Python-3.6%20%7C%203.7%20%7C%203.8-green)
![](https://img.shields.io/badge/AioHTTP-3.6.2-blue)
![](https://img.shields.io/badge/aiohttp_jinja-1.2.1-blue)
![](https://img.shields.io/badge/Jinja2-2.10.1-blue)
![](https://img.shields.io/badge/Bootstrap-4-blue)
![](https://img.shields.io/badge/version-0.0.1-yellowgreen)


### Features

- aiohttp
- auto filter windows forbidden file names (CON, NUL, COM1...  etc.)
- non blocking upload and download files
- download page with file info
- no control for file sizes


### Requirements

- Python 3.6+
- AioHTTP 3.6+
- aiohttp-jinja 1.2+
- Jinja2 2.10+ 

### Usage

```sh 

  -h, --help            show this help message and exit
  -n HOSTNAME, --hostname HOSTNAME
                        DNS hostname with port, default
                        http://k4m454k.hldns.ru:19100
  -p PORT, --port PORT  TCP port number. Default 8090
  -s STORAGE, --storage STORAGE
                        Storage path. Default ./files
```