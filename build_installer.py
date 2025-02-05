import PyInstaller.__main__
import os
import shutil
import subprocess
import sys

def clean_builds():
    """Clean previous builds"""
    for dir_name in ['build', 'dist', 'installer']:
        if os.path.exists(dir_name):
            shutil.rmtree(dir_name)
    if os.path.exists('Imgur Uploader.spec'):
        os.remove('Imgur Uploader.spec')

def build_exe():
    """Build the executable"""
    PyInstaller.__main__.run([
        'imgur_uploader.py',
        '--name=Imgur Uploader',
        '--onefile',
        '--noconsole',
        '--icon=imgur.ico',
        '--add-data=imgur.ico;.',
        '--add-data=imgur.png;.',
        '--add-data=.env;.',
        '--clean',
        '--windowed',
    ])

def build_installer():
    """Build the installer using Inno Setup"""
    # Create installer directory if it doesn't exist
    if not os.path.exists('installer'):
        os.makedirs('installer')
    
    # Get absolute paths
    current_dir = os.path.abspath(os.path.dirname(__file__))
    inno_setup_path = r'C:\Program Files (x86)\Inno Setup 6\ISCC.exe'
    iss_file = os.path.join(current_dir, 'installer.iss')
    
    # Verify Inno Setup exists
    if not os.path.exists(inno_setup_path):
        raise Exception("Inno Setup not found. Please install Inno Setup 6.")
    
    # Run Inno Setup Compiler with proper quoting
    try:
        subprocess.run([inno_setup_path, iss_file], 
                      check=True, 
                      capture_output=True, 
                      text=True)
    except subprocess.CalledProcessError as e:
        print("Error building installer:")
        print(e.stdout)
        print(e.stderr)
        raise

def main():
    try:
        print("Cleaning previous builds...")
        clean_builds()
        
        print("Building executable...")
        build_exe()
        
        print("Building installer...")
        build_installer()
        
        print("Build complete! Installer is in the 'installer' directory.")
    except Exception as e:
        print(f"Error during build: {str(e)}")
        sys.exit(1)

if __name__ == '__main__':
    main() 