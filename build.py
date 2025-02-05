import PyInstaller.__main__
import os
import shutil

# Clean previous builds
for dir_name in ['build', 'dist']:
    if os.path.exists(dir_name):
        shutil.rmtree(dir_name)

# Create executable with PyInstaller
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

# Clean up after build
if os.path.exists('Imgur Uploader.spec'):
    os.remove('Imgur Uploader.spec') 