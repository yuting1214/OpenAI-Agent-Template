import sys
import argparse
from src.app.core.config import get_settings

# Set up the argument parser
parser = argparse.ArgumentParser()
parser.add_argument("--mode", choices=["dev", "prod"], default="dev", help="Set the running mode")
parser.add_argument("--host", type=str, default="127.0.0.1", help="Set the host")

# Determine if running under pytest
is_testing = "pytest" in sys.argv[0]

if is_testing:
    # Provide default or mock arguments when imported for testing
    args = argparse.Namespace(mode="dev", host="127.0.0.1")
else:
    # Parse arguments only when running the script directly
    args = parser.parse_args()

# Initialize and update settings
settings = get_settings(args.mode)

# Save updated settings for import in other modules
global_settings = settings
