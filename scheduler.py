# scheduler.py
import schedule
import time
import subprocess
import sys
import os
from datetime import datetime

def run_pipeline():
    """Run the complete IMDb pipeline"""
    print(f"Starting scheduled run at {datetime.now()}")
    
    try:
        result = subprocess.run([sys.executable, "main.py"], 
                              capture_output=True, 
                              text=True,
                              timeout=3600)
        
        if result.returncode == 0:
            print("Scraping completed successfully!")
            # Only show actual error messages, not info logs
            if result.stderr and any("ERROR" in line for line in result.stderr.split('\n')):
                print("Errors detected:", result.stderr)
            else:
                print("Log output:", result.stdout)
        else:
            print("Scraping failed!")
            print("Error output:", result.stderr)
            
    except subprocess.TimeoutExpired:
        print("Pipeline timed out after 1 hour")
    except Exception as e:
        print(f"Unexpected error: {e}")

# Schedule jobs
schedule.every().day.at("16:00").do(run_pipeline)  # Daily at 4 PM GMT
#schedule.every().sunday.at("02:00").do(run_pipeline)  # Weekly Sunday at 2 AM

print("IMDb Auto-Scraper Started!")
print("Scheduled: Daily at 16:00 GMT, Weekly Sunday at 02:00")
print("Press Ctrl+C to stop")

# Keep running
try:
    while True:
        schedule.run_pending()
        time.sleep(60)
except KeyboardInterrupt:
    print("\n👋 Stopped by user")