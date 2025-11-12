from flask import Flask, jsonify
from exts import db, migrate
from flask_cors import CORS
import config
from contact import bp as contact_bp
from sqlalchemy import text

# 初始化Flask应用
app = Flask(__name__)
app.config.from_object(config.Config)

# 初始化扩展
db.init_app(app)
migrate.init_app(app, db)  # 数据库迁移

# 部署到阿里云服务器的CORS配置
CORS(app, resources={r"/api/*": {
    "origins": [
        "http://121.43.124.28",
        "http://localhost",
        "http://127.0.0.1"
    ],
    "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    "allow_headers": ["Content-Type", "Authorization"]
}})

# 注册蓝图（联系人接口）
app.register_blueprint(contact_bp)

# 健康检查接口（用于验证后端是否可达）
@app.route("/api/health", methods=['GET'])
def health_check():
    return jsonify({"code": 200, "status": "ok", "message": "服务正常运行"})

# 数据库连接测试（启动时验证数据库是否正常）
with app.app_context():
    try:
        db.session.execute(text('SELECT 1'))
        print("数据库连接成功！")
    except Exception as e:
        print(f"数据库连接失败：{str(e)}")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=7894, debug=False)  # 端口改为7894