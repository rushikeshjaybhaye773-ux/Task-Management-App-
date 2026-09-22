from flask import Blueprint, request, jsonify
from services.supabase_client import supabase
from services.gmail_service import send_task_notification
import datetime

tasks_bp = Blueprint('tasks', __name__)

@tasks_bp.route('', methods=['GET'])
@tasks_bp.route('/', methods=['GET'])
def get_tasks():
    user_id = request.args.get('user_id')
    if not user_id:
        return jsonify({"error": "user_id is required"}), 400
        
    try:
        # Get tasks created by user OR assigned to user
        response = supabase.table('tasks').select('*, created_by(*), assigned_to(*)').or_(f'created_by.eq.{user_id},assigned_to.eq.{user_id}').order('created_at', desc=True).execute()
        return jsonify(response.data), 200
    except Exception as e:
        return jsonify({"error": "Failed to fetch tasks", "details": str(e)}), 500

@tasks_bp.route('', methods=['POST'])
@tasks_bp.route('/', methods=['POST'])
def create_task():
    data = request.json
    title = data.get('title')
    description = data.get('description')
    created_by = data.get('created_by')
    assigned_to = data.get('assigned_to')
    
    if not title or not created_by:
        return jsonify({"error": "Title and created_by are required"}), 400
        
    try:
        new_task = {
            'title': title,
            'description': description,
            'created_by': created_by,
            'assigned_to': assigned_to,
            'status': 'PENDING'
        }
        response = supabase.table('tasks').insert(new_task).execute()
        task = response.data[0]
        
        # Send Gmail notification
        if assigned_to and assigned_to != created_by:
            # Get assigned user's email
            assignee = supabase.table('users').select('email, name').eq('id', assigned_to).execute()
            if assignee.data:
                assignee_email = assignee.data[0]['email']
                assignee_name = assignee.data[0]['name']
                subject = "New Task Assigned"
                body = f"Hi {assignee_name},\n\nYou have been assigned a new task.\nTask: {title}\nDescription: {description}\n\nPlease login to the Task Management application to view and complete the task."
                send_task_notification(assignee_email, subject, body)
                
        return jsonify(task), 201
    except Exception as e:
        return jsonify({"error": "Failed to create task", "details": str(e)}), 500

@tasks_bp.route('/<task_id>/complete', methods=['PUT'])
def complete_task(task_id):
    try:
        response = supabase.table('tasks').update({
            'status': 'COMPLETED',
            'completed_at': datetime.datetime.utcnow().isoformat()
        }).eq('id', task_id).execute()
        
        if not response.data:
            return jsonify({"error": "Task not found"}), 404
            
        task = response.data[0]
        
        # Notify creator
        creator_id = task['created_by']
        assigned_to = task['assigned_to']
        
        if creator_id != assigned_to:
            creator = supabase.table('users').select('email, name').eq('id', creator_id).execute()
            assignee = supabase.table('users').select('name').eq('id', assigned_to).execute()
            
            if creator.data and assignee.data:
                creator_email = creator.data[0]['email']
                creator_name = creator.data[0]['name']
                assignee_name = assignee.data[0]['name']
                
                subject = "Task Completed"
                body = f"Hi {creator_name},\n\nThe task '{task['title']}' has been completed by {assignee_name}."
                send_task_notification(creator_email, subject, body)
                
        return jsonify(task), 200
    except Exception as e:
        return jsonify({"error": "Failed to complete task", "details": str(e)}), 500
