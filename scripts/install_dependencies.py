import subprocess
import sys

def install_dependencies():
    """Simple script to install all required dependencies"""
    
    packages = [
        "fastapi",
        "uvicorn[standard]", 
        "python-multipart",
        "pillow",
        "numpy",
        "opencv-python",
        "mediapipe"
    ]
    
    print("Installing Python dependencies for Sign Language Detection...")
    print("This may take a few minutes...")
    
    for package in packages:
        print(f"\nInstalling {package}...")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", package])
            print(f"✓ {package} installed successfully")
        except subprocess.CalledProcessError:
            print(f"✗ Failed to install {package}")
            print("You may need to install it manually:")
            print(f"pip install {package}")

if __name__ == "__main__":
    install_dependencies()
    print("\n🎉 Installation complete!")
    print("Now run: python scripts/sign_detection_server.py")
