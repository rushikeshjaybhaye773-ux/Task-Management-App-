from flask import Blueprint, request, jsonify
from google.oauth2 import id_token
from google.auth.transport import requests
from services.supabase_client import supabase
from config import Config
import os

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/google', methods=['POST'])
def google_auth():
    data = request.json
    token = data.get('token')
    
    if not token:
        return jsonify({"error": "No token provided"}), 400
        
    try:
        # Specify the CLIENT_ID of the app that accesses the backend:
        idinfo = id_token.verify_oauth2_token(
            token, 
            requests.Request(), 
            Config.GOOGLE_CLIENT_ID,
            clock_skew_in_seconds=10
        )

        # ID token is valid. Get the user's Google Account ID from the decoded token.
        google_id = idinfo['sub']
        email = idinfo['email']
        name = idinfo.get('name', '')
        picture = idinfo.get('picture', '')
        
        # Check if user exists in Supabase
        user_response = supabase.table('users').select('*').eq('google_id', google_id).execute()
        
        if not user_response.data:
            # Create user
            new_user = {
                'google_id': google_id,
                'email': email,
                'name': name,
                'profile_image': picture
            }
            inserted_user = supabase.table('users').insert(new_user).execute()
            user = inserted_user.data[0]
        else:
            user = user_response.data[0]
            
        return jsonify({
            "message": "Authenticated successfully",
            "user": user
        }), 200

    except ValueError as e:
        # Invalid token
        print("ValueError validating token:", str(e))
        return jsonify({"error": "Invalid token", "details": str(e)}), 401
    except Exception as e:
        print("Exception validating token:", str(e))
        return jsonify({"error": "Internal server error", "details": str(e)}), 500
