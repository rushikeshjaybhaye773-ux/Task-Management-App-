from flask import Flask, jsonify
from flask_cors import CORS
from config import Config

def create_app():
    app = Flask(__name__)
    CORS(app)
    app.config.from_object(Config)

    # Register blueprints (routes)
    from routes.auth import auth_bp
    from routes.tasks import tasks_bp
    from routes.users import users_bp
    
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(tasks_bp, url_prefix='/api/tasks')
    app.register_blueprint(users_bp, url_prefix='/api/users')

    @app.route("/api/health")
    def health_check():
        return jsonify({"status": "healthy"}), 200

    return app

app = create_app()

if __name__ == "__main__":
    app.run(debug=True, port=5000)
