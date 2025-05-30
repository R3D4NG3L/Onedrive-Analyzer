import os
import sys
from flask import Flask
from flask_cors import CORS

# Add the project directory to Python path
project_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_dir)

# Import our local modules
from utils.config import load_config
from utils.api_routes import init_routes
from utils.database import init_db, close_db

def create_app():
    """Create and configure the Flask application"""
    # Load configuration
    config = load_config()

    # Create Flask app
    app = Flask(__name__, 
                static_folder='static', 
                template_folder='templates')
    
    # Enable CORS
    CORS(app)
    
    # Make data directory if it doesn't exist
    data_dir = os.path.join(project_dir, 'data')
    os.makedirs(data_dir, exist_ok=True)
    
    # Initialize database
    try:
        print("Initializing database...")
        init_db()
        print("Database initialization complete!")
    except Exception as e:
        print(f"Error initializing database: {e}")
    
    # Register database close function
    app.teardown_appcontext(close_db)

    # Initialize routes
    init_routes(app)

    return app

# Create the app
app = create_app()

if __name__ == '__main__':
    # Run the application
    app.run(debug=True)
