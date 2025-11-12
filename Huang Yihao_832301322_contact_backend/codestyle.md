# 联系人管理系统 - 后端代码风格规范 (codestyle.md)

## 1. 通用规范
# 编码格式
- 所有 Python 文件统一使用 **UTF-8 编码**，文件末尾保留 1 个空行
- 缩进使用 **4 个空格**（禁止使用制表符 `Tab`），确保跨编辑器格式一致
- 每行代码长度控制在 **80-120 字符** 以内，超长代码需合理换行（优先在逗号、运算符后换行）
- 代码块之间保留 **1 个空行** 分隔（如函数之间、类定义之间），同一函数内逻辑块之间可保留 1 个空行


## 2. Python 代码规范（核心框架）
### 2.1 导入规范
- 导入顺序：标准库 → 第三方库 → 项目本地模块，不同类别之间用空行分隔
- 导入方式：
  - 禁止使用 `from module import *`（避免命名污染）
  - 单个模块导入多个元素时，用逗号分隔并换行（如 `from flask import Flask, jsonify, request`）
  - 长导入语句可使用括号换行，示例：
    ```python
    from flask_sqlalchemy import SQLAlchemy
    from flask_migrate import Migrate
    from flask_cors import CORS  # 第三方库与本地模块空行分隔
    from exts import db, migrate
    from contact import bp as contact_bp