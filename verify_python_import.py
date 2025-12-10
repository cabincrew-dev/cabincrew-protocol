import sys
import os

# Add lib/python/src to path
sys.path.append(os.path.join(os.getcwd(), "lib/python/src"))

try:
    import cabincrew_protocol
    from cabincrew_protocol import artifact, audit, engine, orchestrator, plantoken
    # Check if helpers are present?
    # e.g. from_str
    print("Imports successful.")
except ImportError as e:
    print(f"ImportError: {e}")
    sys.exit(1)
except Exception as e:
    print(f"Error: {e}")
    sys.exit(1)
