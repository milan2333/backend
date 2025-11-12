from flask import Blueprint, request, jsonify
from exts import db
from models import Contact, ContactVersion
from datetime import datetime
import traceback

bp = Blueprint('contact', __name__, url_prefix='/api/contacts')

# 创建联系人
@bp.route('/add', methods=['POST'])
def add_contact():
    try:
        data = request.get_json()
        name = data.get('name', '').strip()
        phone = data.get('phone', '').strip()
        if not name:
            return jsonify({'code': 400, 'message': '联系人姓名不能为空！'})
        if not phone:
            return jsonify({'code': 400, 'message': '手机号不能为空！'})
        if Contact.query.filter_by(phone=phone).first():
            return jsonify({'code': 400, 'message': f'手机号「{phone}」已存在！'})
        new_contact = Contact(name=name, phone=phone)
        db.session.add(new_contact)
        db.session.flush()  # 获取自增ID
        # 初始化版本记录
        initial_version = ContactVersion(
            contact_id=new_contact.id,
            name=name,
            phone=phone
        )
        db.session.add(initial_version)
        db.session.commit()
        return jsonify({
            'code': 200,
            'message': f'联系人「{name}」创建成功',
            'data': new_contact.to_dict()
        })
    except Exception as e:
        db.session.rollback()
        traceback.print_exc()
        return jsonify({'code': 500, 'message': f'创建失败：{str(e)}'})

# 获取所有联系人（关键修改：新增带斜杠的路由，兼容 /api/contacts 和 /api/contacts/）
@bp.route('', methods=['GET'])       # 原路由：匹配 /api/contacts
@bp.route('/', methods=['GET'])      # 新增路由：匹配 /api/contacts/
def get_contacts():
    try:
        contacts = Contact.query.order_by(Contact.created_time.desc()).all()
        return jsonify({
            'code': 200,
            'data': [c.to_dict() for c in contacts],
            'message': '查询成功'
        })
    except Exception as e:
        return jsonify({'code': 500, 'message': f'查询失败：{str(e)}'})

# 获取单个联系人
@bp.route('/<int:contact_id>', methods=['GET'])
def get_contact(contact_id):
    try:
        contact = Contact.query.get(contact_id)
        if not contact:
            return jsonify({'code': 404, 'message': '联系人不存在'})
        return jsonify({
            'code': 200,
            'data': contact.to_dict(),
            'message': '查询成功'
        })
    except Exception as e:
        return jsonify({'code': 500, 'message': f'查询失败：{str(e)}'})

# 更新联系人
@bp.route('/<int:contact_id>/update', methods=['PUT'])
def update_contact(contact_id):
    contact = Contact.query.get(contact_id)
    if not contact:
        return jsonify({'code': 404, 'message': '联系人不存在'})
    try:
        data = request.get_json()
        name = data.get('name', '').strip()
        phone = data.get('phone', '').strip()
        if not name:
            return jsonify({'code': 400, 'message': '联系人姓名不能为空！'})
        if not phone:
            return jsonify({'code': 400, 'message': '手机号不能为空！'})
        # 验证新手机号是否被其他联系人使用
        if Contact.query.filter(Contact.phone == phone, Contact.id != contact_id).first():
            return jsonify({'code': 400, 'message': f'手机号「{phone}」已存在！'})
        # 记录旧数据
        old_name = contact.name
        old_phone = contact.phone
        # 更新主表
        contact.name = name
        contact.phone = phone
        contact.updated_time = datetime.now()
        # 有变更则创建版本记录
        if old_name != name or old_phone != phone:
            new_version = ContactVersion(
                contact_id=contact.id,
                name=name,
                phone=phone
            )
            db.session.add(new_version)
        db.session.commit()
        return jsonify({
            'code': 200,
            'data': contact.to_dict(),
            'message': '更新成功'
        })
    except Exception as e:
        db.session.rollback()
        traceback.print_exc()
        return jsonify({'code': 500, 'message': f'更新失败：{str(e)}'})

# 删除联系人
@bp.route('/<int:contact_id>/delete', methods=['DELETE'])
def delete_contact(contact_id):
    contact = Contact.query.get(contact_id)
    if not contact:
        return jsonify({'code': 404, 'message': '联系人不存在'})
    try:
        db.session.delete(contact)
        db.session.commit()
        return jsonify({'code': 200, 'message': f'联系人「{contact.name}」删除成功'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'code': 500, 'message': f'删除失败：{str(e)}'})

# 获取联系人版本历史
@bp.route('/<int:contact_id>/versions', methods=['GET'])
def contact_versions(contact_id):
    contact = Contact.query.get(contact_id)
    if not contact:
        return jsonify({'code': 404, 'message': '联系人不存在'})
    versions = ContactVersion.query.filter_by(contact_id=contact_id).order_by(ContactVersion.update_time.desc()).all()
    return jsonify({
        'code': 200,
        'data': [v.to_dict() for v in versions],
        'message': '版本历史查询成功'
    })