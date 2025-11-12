class Config:
    # 数据库配置（替换为阿里云服务器的实际数据库信息）
    HOSTNAME = "127.0.0.1"  # 如果是云数据库，使用云数据库内网地址
    PORT = 3306
    USERNAME = "contact"  # 你的数据库用户名
    PASSWORD = "912c6fff7717a629"  # 你的数据库密码
    DATABASE = "contact"  # 数据库名称（需提前创建）
    SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://{USERNAME}:{PASSWORD}@{HOSTNAME}:{PORT}/{DATABASE}?charset=utf8mb4"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = False
    # Flask配置
    DEBUG = False  # 生产环境关闭调试模式
    SECRET_KEY = "contact_api_secret_key_production"  # 生产环境使用更强的密钥