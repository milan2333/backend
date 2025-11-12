# 项目目录（替换为阿里云服务器的实际项目路径）
chdir = '/www/wwwroot/contact_api'
# 进程数
workers = 4
# 线程数
threads = 2
# 启动用户
user = 'www'
# 启动模式
worker_class = 'sync'
# 绑定地址端口 - 改为7894
bind = '0.0.0.0:7894'
# 进程文件
pidfile = '/www/wwwroot/contact_api/gunicorn.pid'
# 日志路径（需提前创建目录）
accesslog = '/www/wwwlogs/contact_api/access.log'
errorlog = '/www/wwwlogs/contact_api/error.log'
# 日志级别
loglevel = 'info'