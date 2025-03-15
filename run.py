"""
MCLG-WS Launcher
This script properly sets up the Python path and launches the application.
"""
import os
import sys
import subprocess
from pathlib import Path

# Add the project root to Python's path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

# Import and run the main function
if __name__ == "__main__":
    try:
        app_path = project_root / "app" / "app.py"
        subprocess.run([sys.executable, "-m", "streamlit", "run", str(app_path)])
    except Exception as e:
        print(f"Error launching application: {e}")
        
"""
        Removing the following approach to test simpler one
       
       # Use this approach to avoid circular imports
        import streamlit.web.cli as stcli
        
        # Run the Streamlit app with proper module path
        sys.argv = ["streamlit", "run", str(project_root / "app" / "app.py")]
        stcli.main()
    except Exception as e:
        print(f"Error launching application: {e}")
"""

        
