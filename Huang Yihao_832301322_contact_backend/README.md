# 联系人管理系统 - 后端 README.md

## 项目介绍
本项目是联系人管理系统的后端服务，基于 Flask 框架开发，提供 RESTful API 接口，实现联系人的增删改查及版本历史记录功能，支持与前端页面交互，数据存储于 MySQL 数据库。

## 项目结构
```
backend/
├── src\
    ├── app.py              # 应用入口文件
    ├── config.py           # 配置文件
    ├── contact.py          # 联系人接口蓝图
    ├── models.py           # 数据模型
    ├── exts.py             # 扩展初始化
    ├── create_tables.py    # 数据库表创建脚本
    ├── requirements.txt    # 依赖包列表
    ├── gunicorn.conf.py    # Gunicorn配置文件（生产环境部署）
├── codestyle.md        # 代码风格文档
└── README.md           # 项目说明文档
```

## 技术栈
框架：Flask 2.2.3
数据库：MySQL + SQLAlchemy 3.0.3（ORM）
数据库迁移：Flask-Migrate 4.0.4
跨域支持：Flask-CORS 3.0.10
生产环境部署：Gunicorn 20.1.0
数据库驱动：pymysql 1.0.2

## 核心功能
### 1. 联系人管理
新增联系人：验证姓名和手机号非空，手机号唯一
查询所有联系人：按创建时间倒序返回
查询单个联系人：根据 ID 查询详情
更新联系人：验证手机号唯一性，自动记录版本历史
删除联系人：删除主记录及关联的版本记录（级联删除）
### 2. 版本历史记录
新增联系人时自动创建初始版本记录
更新联系人时对比旧数据，有变更则创建新版本记录
支持查询指定联系人的所有版本历史（含操作人、更新时间）
### 3. 系统保障
健康检查接口：/api/health 验证服务是否正常运行
数据库连接测试：启动时自动执行 SELECT 1 验证连接状态
异常处理：所有接口均有异常捕获，返回统一格式错误信息（code + message + data）
事务管理：数据操作失败时自动回滚，保证数据一致性
跨域支持：允许 http://121.43.124.28、http://localhost、http://127.0.0.1 访问
## API 接口文档
# API 接口文档

| 接口路径 | 请求方法 | 功能描述 | 请求参数| 返回格式示例                                                                 |
|-------------------------|----------|------------------------|-----------------------------------|------------------------------------------------------------------------------|
| `/api/health`           | GET      | 服务健康检查           | 无                                | `{"code":200,"status":"ok","message":"服务正常运行"}`                        |
| `/api/contacts`         | GET      | 获取所有联系人         | 无                                | `{"code":200,"message":"success","data":[{"id":1,"name":"张三","phone":"13800138000","created_time":"2024-01-01 10:00:00","updated_time":"2024-01-01 10:00:00"}]}` |
| `/api/contacts/{id}`    | GET      | 获取单个联系人         | 路径参数：`id`（联系人 ID，整数类型） | `{"code":200,"message":"success","data":{"id":1,"name":"张三","phone":"13800138000","created_time":"2024-01-01 10:00:00","updated_time":"2024-01-01 10:00:00"}}` |
| `/api/contacts/add`     | POST     | 添加联系人             | JSON 体：<br>`name`（联系人姓名，非空）<br>`phone`（联系人手机号，非空且唯一） | `{"code":200,"message":"添加联系人成功","data":{"id":1,"name":"张三","phone":"13800138000","created_time":"2024-01-01 10:00:00","updated_time":"2024-01-01 10:00:00"}}` |
| `/api/contacts/{id}/update` | PUT   | 更新联系人             | 1. 路径参数：`id`（联系人 ID，整数类型）<br>2. JSON 体：<br>`name`（新姓名，非空）<br>`phone`（新手机号，非空且唯一） | `{"code":200,"message":"更新联系人成功","data":{"id":1,"name":"张三更新","phone":"13800138001","created_time":"2024-01-01 10:00:00","updated_time":"2024-01-01 11:00:00"}}` |
| `/api/contacts/{id}/delete` | DELETE  | 删除联系人             | 路径参数：`id`（联系人 ID，整数类型） | `{"code":200,"message":"删除联系人成功"}`                                    |
| `/api/contacts/{id}/versions` | GET    | 获取联系人版本历史     | 路径参数：`id`（联系人 ID，整数类型） | `{"code":200,"message":"查询成功","data":[{"id":1,"contact_id":1,"name":"张三","phone":"13800138000","update_time":"2024-01-01 10:00:00","operator":"system"}]}` |

## 部署说明
### 1. 环境准备
- Python 版本：3.7+
- 安装依赖：`pip install -r requirements.txt`
- MySQL 数据库：提前创建数据库（默认库名：`contact`）

### 2. 配置修改
#### 2.1 编辑 `config.py` 文件（默认已配置，无需手动修改）：
```python
class Config:
    # 数据库配置（阿里云服务器实际配置）
    HOSTNAME = "127.0.0.1"  # 云数据库请替换为内网地址
    PORT = 3306
    USERNAME = "contact"     # 数据库用户名
    PASSWORD = "912c6fff7717a629"  # 数据库密码
    DATABASE = "contact"     # 数据库名称
    SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://{USERNAME}:{PASSWORD}@{HOSTNAME}:{PORT}/{DATABASE}?charset=utf8mb4"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = False
    # Flask配置
    DEBUG = False  # 生产环境已关闭调试模式
    SECRET_KEY = "contact_api_secret_key_production"  # 生产环境密钥
```
### 2.2 编辑 `gunicorn.conf.py` 文件（默认已配置阿里云路径）：
```python
# 项目目录（阿里云服务器实际路径，指向后端代码根目录）
chdir = '/www/wwwroot/contact_api'

# 进程数配置（根据服务器CPU核心数调整，4进程适配多数轻量云服务器）
workers = 4

# 线程数配置（每个进程开启2个线程，提升并发处理能力）
threads = 2

# 启动用户（使用服务器www用户，避免root权限风险）
user = 'www'

# 启动模式（sync为同步模式，稳定适配Flask应用）
worker_class = 'sync'

# 绑定地址与端口（0.0.0.0允许外部访问，默认端口7894）
bind = '0.0.0.0:7894'

# 进程文件路径（用于后续停止/重启服务，记录进程ID）
pidfile = '/www/wwwroot/contact_api/gunicorn.pid'

# 访问日志路径（记录所有请求详情，阿里云服务器标准日志目录）
accesslog = '/www/wwwlogs/python/contact_api/gunicorn_acess.log'

# 错误日志路径（记录服务异常信息，便于问题排查）
errorlog = '/www/wwwlogs/python/contact_api/gunicorn_error.log'

# 日志级别（info级别记录关键操作，兼顾日志完整性与体积）
loglevel = 'info'
```

### 3. 数据库初始化
```bash
# 执行表创建脚本（推荐首次部署使用）
python create_tables.py

# 或使用Flask-Migrate迁移（后续表结构变更用）
flask db init    # 初始化迁移环境（首次执行）
flask db migrate -m "初始化数据库"  # 创建迁移脚本
flask db upgrade  # 执行迁移，创建表
```
### 4. 启动服务
#### 4.1 开发环境
```bash
python app.py  # 启动内置服务器，默认端口7894，访问 http://localhost:7894
```
#### 4.2 生产环境（Gunicorn）
```bash
# 启动服务
gunicorn -c gunicorn.conf.py app:app

# 停止服务
pkill -F /www/wwwroot/contact_api/gunicorn.pid

# 重启服务
pkill -F /www/wwwroot/contact_api/gunicorn.pid && gunicorn -c gunicorn.conf.py app:app
```

## 注意事项
### 1.生产环境已默认关闭 DEBUG 模式（config.py 中 DEBUG=False），无需修改
### 2.数据库密码已配置为 912c6fff7717a629，建议定期更换为更强密码
### 3.日志目录（/www/wwwlogs/python/contact_api/）需提前创建，确保 www 用户有写入权限
### 4.部署在阿里云服务器时，需开放 7894 端口的防火墙规则
### 5.定期备份 MySQL 数据库（contact 库），防止数据丢失
### 6.跨域已默认允许 http://121.43.124.28、http://localhost、http://127.0.0.1，新增域名需修改 app.py 中的 CORS 配置

## 常见问题
### 1.数据库连接失败：检查 MySQL 服务是否启动，config.py 中的用户名、密码、库名是否正确，网络是否通畅
### 2.接口访问跨域：确认 app.py 中的 CORS 配置是否包含前端域名，新增域名需添加到 origins 列表
### 3.启动失败提示端口被占用：修改 app.py、gunicorn.conf.py、uwsgi.ini 中的端口（默认 7894），更换未被占用的端口
### 4.接口返回 500 错误：查看日志文件（gunicorn_error.log 或 uwsgi.log），根据错误信息排查（常见原因：数据库操作失败、参数错误）
### 5.创建表失败：检查 create_tables.py 中依赖文件（app.py、config.py、exts.py、models.py）是否存在，路径是否正确
