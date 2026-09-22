from flask import Blueprint, jsonify
from services.supabase_client import supabase

users_bp = Blueprint('users', __name__)

@users_bp.route('/', methods=['GET'])
def get_users():
    try:
        response = supabase.table('users').select('id, name, email, profile_image').execute()
        return jsonify(response.data), 200
    except Exception as e:
        return jsonify({"error": "Failed to fetch users", "details": str(e)}), 500
