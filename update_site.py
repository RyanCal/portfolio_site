import subprocess
import os
from datetime import datetime


def update_from_git():
    """
    Updates the website code from Git repository and logs the process
    Returns True if successful, False otherwise
    """
    # Directory where your website code lives
    website_dir = "/home/RyanCal/portfolio_site"

    # Log file path
    log_file = os.path.join(website_dir, "git_update.log")

    try:
        # Change to website directory
        os.chdir("/home/RyanCal/portfolio_site")

        # Log the update attempt
        with open(log_file, "a") as f:
            f.write(f"\n[{datetime.now()}] Starting git pull\n")

        # Fetch and pull changes
        subprocess.run(["git", "fetch", "--all"], check=True)
        pull_result = subprocess.run(["git", "pull"],
                                     capture_output=True,
                                     text=True,
                                     check=True)

        # Log the results
        with open(log_file, "a") as f:
            f.write(f"Git pull output: {pull_result.stdout}\n")
            if pull_result.stderr:
                f.write(f"Errors (if any): {pull_result.stderr}\n")
            f.write("Update completed successfully\n")

        # Touch the WSGI file to reload the web app
        wsgi_file = "/var/www/ryancal_pythonanywhere_com_wsgi.py"
        subprocess.run(["touch", wsgi_file], check=True)

        return True

    except Exception as e:
        # Log any errors
        with open(log_file, "a") as f:
            f.write(f"Error occurred: {str(e)}\n")
        return False


if __name__ == "__main__":
    success = update_from_git()
    print("Update successful" if success else "Update failed - check logs")