import sys
import os

# 添加当前目录到Python路径
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

print("开始创建数据库表...")

try:
    from flask import Flask
    import config
    from exts import db
    from models import Contact, ContactVersion
    
    app = Flask(__name__)
    app.config.from_object(config.Config)
    db.init_app(app)
    
    with app.app_context():
        # 创建所有表
        db.create_all()
        print("✅ 数据库表创建成功！")
        
        # 检查创建的表
        from sqlalchemy import inspect
        inspector = inspect(db.engine)
        tables = inspector.get_table_names()
        print(f"✅ 创建的数据库表: {tables}")
        
except ImportError as e:
    print(f"❌ 导入错误: {e}")
    print("请检查以下文件是否存在:")
    print("- app.py")
    print("- config.py") 
    print("- exts.py")
    print("- models.py")
    print("- contact.py")
except Exception as e:
    print(f"❌ 创建表失败: {e}")
