#!/usr/bin/env python3
"""
Script to train the fraud detection model.
"""

import sys
from pathlib import Path

# Add the server and ml directories to the path
sys.path.append(str(Path(__file__).parent.parent / "server"))
sys.path.append(str(Path(__file__).parent.parent / "ml"))

from ml.train import train_fraud_model

def main():
    """Main training function"""
    print("Training fraud detection model...")

    try:
        model_path = train_fraud_model()
        print(f"Model trained and saved to: {model_path}")
        print("Training completed successfully!")
    except Exception as e:
        print(f"Error training model: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()