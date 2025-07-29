import sys
import subprocess

print("🔍 Checking Python Environment")
print("=" * 40)

# Check Python version
print(f"Python version: {sys.version}")
print(f"Python executable: {sys.executable}")

# Check if pip is available
try:
    import pip
    print("✓ pip is available")
except ImportError:
    print("✗ pip is not available")

# Try to check installed packages
try:
    result = subprocess.run([sys.executable, "-m", "pip", "list"], 
                          capture_output=True, text=True, timeout=10)
    if result.returncode == 0:
        print("✓ pip list command works")
        # Check for our required packages
        installed = result.stdout.lower()
        packages = ["fastapi", "uvicorn", "opencv-python", "mediapipe", "pillow", "numpy"]
        
        print("\n📦 Package Status:")
        for pkg in packages:
            if pkg in installed:
                print(f"✓ {pkg} - installed")
            else:
                print(f"✗ {pkg} - not installed")
    else:
        print("✗ pip list command failed")
        print(f"Error: {result.stderr}")
        
except Exception as e:
    print(f"✗ Error checking packages: {e}")

print("\n💡 Manual Installation Commands:")
print("Copy and paste these commands in your terminal:")
print("-" * 40)
print("pip install fastapi")
print("pip install uvicorn")
print("pip install opencv-python")
print("pip install mediapipe") 
print("pip install pillow")
print("pip install numpy")
print("pip install python-multipart")
