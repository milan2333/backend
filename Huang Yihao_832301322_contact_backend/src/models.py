from exts import db
from datetime import datetime

# 联系人主表
class Contact(db.Model):
    __tablename__ = 'contacts'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50), nullable=False)
    phone = db.Column(db.String(20), unique=True, nullable=False)
    created_time = db.Column(db.DateTime, default=datetime.now)
    updated_time = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)
    # 版本记录关联
    versions = db.relationship('ContactVersion', backref='contact', lazy=True, cascade="all, delete-orphan")

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'phone': self.phone,
            'created_time': self.created_time.strftime('%Y-%m-%d %H:%M:%S'),
            'updated_time': self.updated_time.strftime('%Y-%m-%d %H:%M:%S') if self.updated_time else None
        }

# 联系人版本记录表
class ContactVersion(db.Model):
    __tablename__ = 'contact_version'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    contact_id = db.Column(db.Integer, db.ForeignKey('contacts.id'), nullable=False)
    name = db.Column(db.String(50), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    update_time = db.Column(db.DateTime, default=datetime.now)
    operator = db.Column(db.String(50), default="system")

    def to_dict(self):
        return {
            'id': self.id,
            'contact_id': self.contact_id,
            'name': self.name,
            'phone': self.phone,
            'update_time': self.update_time.strftime('%Y-%m-%d %H:%M:%S'),
            'operator': self.operator
        }