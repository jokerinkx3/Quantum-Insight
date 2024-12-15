import os
import logging
from flask import Flask
from flask_cors import CORS
from api.routes import api_bp

def create_app():
    # Configure logging
    logging.basicConfig(level=logging.DEBUG)
    logger = logging.getLogger(__name__)
    
    # Initialize Flask app
    app = Flask(__name__)
    
    # Configure CORS
    CORS(app)
    
    # Set secret key
    app.secret_key = os.environ.get("FLASK_SECRET_KEY", "dev_key")
    
    # Register blueprints
    app.register_blueprint(api_bp, url_prefix='/api')
    
    logger.info("Application initialized successfully")
    return app
