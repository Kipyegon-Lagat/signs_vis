import subprocess
import sys
import os

def check_python_version():
    """Check if Python version is compatible"""
    if sys.version_info < (3, 8):
        print("❌ Python 3.8 or higher is required")
        print(f"Current version: {sys.version}")
        return False
    print(f"✓ Python {sys.version.split()[0]} detected")
    return True

def install_package(package):
    """Install a single package with error handling"""
    try:
        print(f"Installing {package}...")
        subprocess.check_call([
            sys.executable, "-m", "pip", "install", package, "--upgrade"
        ], stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)
        print(f"✓ Successfully installed {package}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"✗ Failed to install {package}")
        if e.stderr:
            print(f"Error: {e.stderr.decode()}")
        return False

def install_requirements():
    """Install required Python packages"""
    print("\n📦 Installing required packages...")
    print("-" * 40)
    
    # Essential packages in order of dependency
    packages = [
        "fastapi",
        "uvicorn[standard]",
        "python-multipart",  # Required for file uploads
        "pillow",
        "numpy",
        "opencv-python",
        "mediapipe"
    ]
    
    failed_packages = []
    
    for package in packages:
        if not install_package(package):
            failed_packages.append(package)
    
    if failed_packages:
        print(f"\n❌ Failed to install: {', '.join(failed_packages)}")
        print("\nTry installing manually:")
        for pkg in failed_packages:
            print(f"pip install {pkg}")
        return False
    
    return True

def test_imports():
    """Test if all required modules can be imported"""
    print("\n🧪 Testing imports...")
    
    modules = [
        ("fastapi", "FastAPI"),
        ("uvicorn", "uvicorn"),
        ("cv2", "OpenCV"),
        ("mediapipe", "MediaPipe"),
        ("PIL", "Pillow"),
        ("numpy", "NumPy")
    ]
    
    failed_imports = []
    
    for module, name in modules:
        try:
            __import__(module)
            print(f"✓ {name} imported successfully")
        except ImportError as e:
            print(f"✗ Failed to import {name}: {e}")
            failed_imports.append(name)
    
    return len(failed_imports) == 0

def main():
    print("🚀 Sign Language Detection Backend Setup")
    print("=" * 50)
    
    # Check Python version
    if not check_python_version():
        return
    
    # Install requirements
    if not install_requirements():
        print("\n❌ Setup failed during package installation")
        return
    
    # Test imports
    if not test_imports():
        print("\n❌ Setup failed during import testing")
        return
    
    print("\n✅ Setup completed successfully!")
    print("\n🎯 Next steps:")
    print("1. Start the backend server:")
    print("   python scripts/sign_detection_server.py")
    print("\n2. The server will be available at:")
    print("   http://localhost:8000")
    print("\n3. Start the frontend in another terminal:")
    print("   npm run dev")

if __name__ == "__main__":
    main()
