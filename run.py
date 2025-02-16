import sys
import subprocess
from pathlib import Path
from dotenv import load_dotenv

def main():
    """
    Main function to load environment variables and start the Streamlit application.
    
    - Loads environment variables from a .env file using `load_dotenv()`.
    - Checks if the Streamlit application file exists.
    - Runs the Streamlit application using `subprocess.run()`.
    - Handles errors gracefully, including missing files and process execution failures.
    """
    load_dotenv()  # Load environment variables from .env file

    app_path = Path("src/app/main.py")  # Define the path to the Streamlit application
    
    if not app_path.exists():
        print(f"Error: Could not find {app_path}")  # Print an error message if the file is missing
        sys.exit(1)  # Exit with an error status code
    
    try:
        # Run the Streamlit application with usage statistics disabled
        subprocess.run(["streamlit", "run", str(app_path), "--browser.gatherUsageStats", "false"], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error running Streamlit app: {e}")  # Handle errors during Streamlit execution
        sys.exit(1)  # Exit with an error status code
    except KeyboardInterrupt:
        print("Stopping app!")  # Handle user interruption (Ctrl+C)
        sys.exit(0)  # Exit gracefully

if __name__ == "__main__":
    main()