import sys
import subprocess

def install():
    print("Installing MV-Adapter Extension Dependencies...")
    
    # This runs the pip installer inside Modly's hidden Python environment
    subprocess.check_call([sys.executable, "-m", "pip", "install", "trimesh", "xatlas", "numpy"])
    
    print("Dependencies installed successfully!")

if __name__ == "__main__":
    install()
