#!/usr/bin/env python3
"""Scheduler wrapper to run the Steam Deck notifier at regular intervals"""

import time
import sys
import os
from datetime import datetime
from notifier import main

def setup_args_from_env():
    """Setup sys.argv from environment variables for notifier.py argument parser"""
    args = ['scheduler.py']  # Script name

    csv_dir = os.getenv('CSV_DIR', '')
    if csv_dir:
        args.extend(['--csv-dir', csv_dir])

    country_code = os.getenv('COUNTRY_CODE', 'DE')
    args.extend(['--country-code', country_code])

    webhook_url = os.getenv('WEBHOOK_URL', '')
    if webhook_url:
        args.extend(['--webhook-url', webhook_url])

    role_mapping = os.getenv('ROLE_MAPPING', '')
    if role_mapping:
        args.extend(['--role-mapping', role_mapping])

    sys.argv = args

def run_with_interval(interval_minutes: int):
    """Run the notifier at specified intervals

    Args:
        interval_minutes: Minutes between each check
    """
    print(f"Starting Steam Deck notifier scheduler", flush=True)
    print(f"Check interval: {interval_minutes} minutes", flush=True)
    print(f"Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", flush=True)
    print("-" * 50, flush=True)

    while True:
        try:
            print(f"\n[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Running check...", flush=True)
            setup_args_from_env()
            main()
            print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Check completed. Next check in {interval_minutes} minutes.", flush=True)
        except KeyboardInterrupt:
            print("\nScheduler stopped by user", flush=True)
            sys.exit(0)
        except Exception as e:
            print(f"Error during check: {e}", flush=True)
            import traceback
            traceback.print_exc()
            print(f"Will retry in {interval_minutes} minutes...", flush=True)

        # Sleep for the specified interval
        time.sleep(interval_minutes * 60)

if __name__ == "__main__":
    # Get interval from environment variable or use default
    interval = int(os.getenv('CHECK_INTERVAL_MINUTES', '5'))

    if interval < 1:
        print("Error: CHECK_INTERVAL_MINUTES must be at least 1")
        sys.exit(1)

    run_with_interval(interval)
