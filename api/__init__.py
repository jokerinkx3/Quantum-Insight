import os
import logging
from flask import Flask
from flask_cors import CORS

def create_app():
    # Configure logging
    logging.basicConfig(level=logging.DEBUG)
    logger = logging.getLogger(__name__)
    
    # Initialize Flask app
    app = Flask(__name__, 
                template_folder=os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates'))
    
    # Configure CORS
    CORS(app)
    
    # Set secret key
    app.secret_key = os.environ.get("FLASK_SECRET_KEY", "dev_key")
    
    try:
        # Register blueprints
        from api.routes import api_bp
        app.register_blueprint(api_bp, url_prefix='/api')
        logger.info("Blueprint registered successfully")
    except Exception as e:
        logger.error(f"Error registering blueprint: {str(e)}")
        raise
    
    @app.route('/')
    def index():
        return "Welcome to the Quantum State Analysis API. Visit /api/test for the test interface."
    
    logger.info("Application initialized successfully")
    return app
