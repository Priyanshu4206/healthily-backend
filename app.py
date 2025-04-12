from flask import Flask
from flask_cors import CORS
from config import load_config
from api.routes import init_routes

def create_app():
    """Create and configure the Flask application"""
    # Load configuration
    config = load_config()
    
    # Create Flask app
    app = Flask(__name__)

    # Enable CORS for all routes
    CORS(app, resources={r"/*": {"origins": "*"}})

    # Register blueprints
    app.register_blueprint(init_routes(config))
    
    return app, config

if __name__ == '__main__':
    # Create the app
    app, config = create_app()
    
    # Start the server
    print(f"Starting server on port {config['port']}...")
    app.run(
        host=config['host'],
        port=config['port'],
        debug=config['debug']
    )