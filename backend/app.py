from flask import Flask, send_from_directory
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_mail import Mail
from backend.config import Config
from backend.models import db
from backend.routes import register_routes
import os

mail = Mail()
jwt = JWTManager()


def create_app():
    app = Flask(__name__, static_folder='../frontend', static_url_path='')
    app.config.from_object(Config)

    db.init_app(app)
    mail.init_app(app)
    jwt.init_app(app)
    CORS(app)

    register_routes(app)

    frontend_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'frontend')

    @app.route('/')
    def index():
        return send_from_directory(os.path.join(frontend_dir, 'pages'), 'login.html')

    @app.route('/pages/<path:filename>')
    def serve_pages(filename):
        return send_from_directory(os.path.join(frontend_dir, 'pages'), filename)

    return app


if __name__ == '__main__':
    app = create_app()
    with app.app_context():
        db.create_all()
    app.run(debug=True, port=5000)
