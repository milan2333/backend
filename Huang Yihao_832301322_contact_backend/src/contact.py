from flask import Blueprint, request, jsonify
from models import Contact, ContactVersion
from exts import db
from datetime import datetime

bp = Blueprint('contact', __name__, url_prefix='/api/contacts')

# Get all contacts
@bp.route('/', methods=['GET'])
def get_contacts():
    try:
        contacts = Contact.query.order_by(Contact.created_time.desc()).all()
        return jsonify({
            "code": 200,
            "message": "success",
            "data": [contact.to_dict() for contact in contacts]
        })
    except Exception as e:
        error_msg = "获取联系人失败：" + str(e)
        return jsonify({
            "code": 500,
            "message": error_msg,
            "data": []
        }), 500

# Get single contact
@bp.route('/<int:contact_id>', methods=['GET'])
def get_contact(contact_id):
    try:
        contact = Contact.query.get(contact_id)
        if not contact:
            return jsonify({
                "code": 404,
                "message": "联系人不存在",
                "data": None
            }), 404
        
        return jsonify({
            "code": 200,
            "message": "success",
            "data": contact.to_dict()
        })
    except Exception as e:
        error_msg = "获取联系人详情失败：" + str(e)
        return jsonify({
            "code": 500,
            "message": error_msg,
            "data": None
        }), 500

# Add contact
@bp.route('/add', methods=['POST'])
def add_contact():
    try:
        data = request.get_json()
        if not data:
            return jsonify({
                "code": 400,
                "message": "请求数据不能为空"
            }), 400
        
        name = data.get('name')
        phone = data.get('phone')
        
        if not name or not phone:
            return jsonify({
                "code": 400,
                "message": "姓名和手机号不能为空"
            }), 400
        
        # Check if phone already exists
        existing_contact = Contact.query.filter_by(phone=phone).first()
        if existing_contact:
            return jsonify({
                "code": 400,
                "message": "手机号已存在"
            }), 400
        
        # Create new contact
        new_contact = Contact(name=name, phone=phone)
        db.session.add(new_contact)
        db.session.commit()
        
        return jsonify({
            "code": 200,
            "message": "添加联系人成功",
            "data": new_contact.to_dict()
        })
        
    except Exception as e:
        db.session.rollback()
        error_msg = "添加联系人失败：" + str(e)
        return jsonify({
            "code": 500,
            "message": error_msg
        }), 500

# Update contact
@bp.route('/<int:contact_id>/update', methods=['PUT'])
def update_contact(contact_id):
    try:
        data = request.get_json()
        if not data:
            return jsonify({
                "code": 400,
                "message": "请求数据不能为空"
            }), 400
        
        contact = Contact.query.get(contact_id)
        if not contact:
            return jsonify({
                "code": 404,
                "message": "联系人不存在"
            }), 404
        
        name = data.get('name')
        phone = data.get('phone')
        
        if not name or not phone:
            return jsonify({
                "code": 400,
                "message": "姓名和手机号不能为空"
            }), 400
        
        # Check if phone is used by other contact
        existing_contact = Contact.query.filter(Contact.phone == phone, Contact.id != contact_id).first()
        if existing_contact:
            return jsonify({
                "code": 400,
                "message": "手机号已被其他联系人使用"
            }), 400
        
        # Save version record
        version = ContactVersion(
            contact_id=contact_id,
            name=contact.name,
            phone=contact.phone,
            operator="system"
        )
        db.session.add(version)
        
        # Update contact info
        contact.name = name
        contact.phone = phone
        contact.updated_time = datetime.now()
        
        db.session.commit()
        
        return jsonify({
            "code": 200,
            "message": "更新联系人成功",
            "data": contact.to_dict()
        })
        
    except Exception as e:
        db.session.rollback()
        error_msg = "更新联系人失败：" + str(e)
        return jsonify({
            "code": 500,
            "message": error_msg
        }), 500

# Delete contact
@bp.route('/<int:contact_id>/delete', methods=['DELETE'])
def delete_contact(contact_id):
    try:
        contact = Contact.query.get(contact_id)
        if not contact:
            return jsonify({
                "code": 404,
                "message": "联系人不存在"
            }), 404
        
        # Delete related version records
        ContactVersion.query.filter_by(contact_id=contact_id).delete()
        # Delete contact
        db.session.delete(contact)
        db.session.commit()
        
        return jsonify({
            "code": 200,
            "message": "删除联系人成功"
        })
        
    except Exception as e:
        db.session.rollback()
        error_msg = "删除联系人失败：" + str(e)
        return jsonify({
            "code": 500,
            "message": error_msg
        }), 500
