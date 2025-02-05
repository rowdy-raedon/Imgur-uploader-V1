import sys, json, os, requests
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QPalette, QColor, QIcon, QPixmap
from dotenv import load_dotenv

class ImgurUploader(QMainWindow):
    def __init__(self):
        super().__init__()
        load_dotenv()
        self.client_id = os.getenv('IMGUR_CLIENT_ID')
        
        # Set application icon
        icon_path = os.path.join(os.path.dirname(__file__), 'imgur.ico')
        if os.path.exists(icon_path):
            self.setWindowIcon(QIcon(icon_path))
            
        self.setup_ui()
        
    def setup_ui(self):
        self.setWindowTitle("Imgur Uploader")
        self.setFixedSize(400, 250)  # Reduced height
        self.setStyleSheet("""
            * { background-color: #2b2b2b; color: white; }
            QPushButton { background-color: #57a1a7; border: none; padding: 8px; border-radius: 4px; }
            QPushButton:hover { background-color: #68b2b8; }
            QLineEdit { background-color: #363636; border: 1px solid #444; padding: 5px; border-radius: 4px; }
            QStatusBar { background-color: #363636; padding: 2px; font-size: 11px; }
            QLabel#credits { color: #888; font-size: 10px; }
            QLabel#logo { padding: 10px; }
        """)
        
        layout = QVBoxLayout()
        layout.setSpacing(8)  # Reduced spacing
        layout.setContentsMargins(10, 10, 10, 10)  # Minimal margins
        central = QWidget()
        central.setLayout(layout)
        self.setCentralWidget(central)
        
        # Logo image instead of text title
        logo_path = os.path.join(os.path.dirname(__file__), 'imgur.png')
        if os.path.exists(logo_path):
            logo_label = QLabel()
            logo_label.setObjectName("logo")
            logo_pixmap = QPixmap(logo_path)
            # Scale the logo to fit nicely in the window (adjust size as needed)
            scaled_pixmap = logo_pixmap.scaled(150, 50, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            logo_label.setPixmap(scaled_pixmap)
            logo_label.setAlignment(Qt.AlignCenter)
            layout.addWidget(logo_label)
        
        # Main UI elements
        self.file_path = QLineEdit()
        self.file_path.setPlaceholderText("No file selected")
        self.file_path.setReadOnly(True)
        
        browse_btn = QPushButton("Browse")
        browse_btn.clicked.connect(self.browse_file)
        
        self.upload_btn = QPushButton("Upload")
        self.upload_btn.clicked.connect(self.upload_image)
        
        self.url_display = QLineEdit()
        self.url_display.setReadOnly(True)
        self.url_display.hide()
        
        self.copy_btn = QPushButton("Copy Link")
        self.copy_btn.clicked.connect(lambda: [
            QApplication.clipboard().setText(self.url_display.text()),
            self.copy_btn.setText("Copied!"),
            QTimer.singleShot(2000, lambda: self.copy_btn.setText("Copy Link"))
        ])
        self.copy_btn.hide()
        
        # Add only the necessary widgets
        for w in [self.file_path, browse_btn, self.upload_btn]:
            layout.addWidget(w)
            
        # Add spacer to push credits to bottom
        layout.addSpacing(5)  # Minimal space before credits
            
        # Add credits at bottom right
        credits = QLabel("Developed with ❤️ by RowdyRaedon")
        credits.setObjectName("credits")
        credits.setAlignment(Qt.AlignRight)
        layout.addWidget(credits)
            
        # Status bar
        self.status_bar = QStatusBar()
        self.status_bar.showMessage("Ready")
        self.setStatusBar(self.status_bar)
        
    def browse_file(self):
        file_name, _ = QFileDialog.getOpenFileName(
            self, "Select Image", "", "Images (*.png *.jpg *.jpeg *.gif *.bmp)"
        )
        if file_name:
            self.file_path.setText(file_name)
            self.url_display.hide()
            self.copy_btn.hide()
            
    def show_upload_success(self, url):
        dialog = QDialog(self)
        dialog.setWindowTitle("Success")
        dialog.setFixedSize(350, 100)  # Smaller size
        
        dialog.setWindowIcon(self.windowIcon())
        
        dialog.setStyleSheet("""
            QDialog { background-color: #2b2b2b; }
            QLabel { color: white; }
            QLineEdit { 
                background-color: #363636; 
                border: 1px solid #444; 
                padding: 8px; 
                border-radius: 4px;
                color: white;
                selection-background-color: #57a1a7;
            }
            QPushButton { 
                background-color: #57a1a7; 
                border: none; 
                padding: 8px; 
                border-radius: 4px;
                color: white;
            }
            QPushButton:hover { 
                background-color: #68b2b8; 
            }
        """)

        layout = QVBoxLayout(dialog)
        layout.setSpacing(10)
        layout.setContentsMargins(15, 15, 15, 15)

        # URL display and copy button in horizontal layout
        url_layout = QHBoxLayout()
        
        url_field = QLineEdit(url)
        url_field.setReadOnly(True)
        url_field.setMinimumWidth(250)
        url_field.setAlignment(Qt.AlignCenter)
        url_layout.addWidget(url_field)

        copy_btn = QPushButton("Copy")
        copy_btn.setFixedWidth(70)
        copy_btn.clicked.connect(lambda: [
            QApplication.clipboard().setText(url),
            copy_btn.setText("✓"),
            QTimer.singleShot(1000, lambda: copy_btn.setText("Copy"))
        ])
        url_layout.addWidget(copy_btn)

        layout.addLayout(url_layout)
        
        # Auto-select URL text
        url_field.selectAll()
        
        dialog.show()
        
    def upload_image(self):
        if not self.file_path.text():
            QMessageBox.warning(self, "Error", "Please select an image first!")
            return
            
        self.upload_btn.setEnabled(False)
        self.upload_btn.setText("Uploading...")
        
        try:
            with open(self.file_path.text(), 'rb') as img:
                response = requests.post(
                    'https://api.imgur.com/3/upload',
                    headers={'Authorization': f'Client-ID {self.client_id}'},
                    files={'image': img},
                    timeout=30
                ).json()
                
            if response['success']:
                url = response['data']['link']
                QApplication.clipboard().setText(url)
                self.show_upload_success(url)
                self.status_bar.showMessage("Upload successful!")
            else:
                raise Exception("Upload failed")
                
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))
            self.status_bar.showMessage("Upload failed!")
            
        finally:
            self.upload_btn.setEnabled(True)
            self.upload_btn.setText("Upload")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    
    # Set application-wide icon
    icon_path = os.path.join(os.path.dirname(__file__), 'imgur.ico')
    if os.path.exists(icon_path):
        app.setWindowIcon(QIcon(icon_path))
    
    # Dark theme
    palette = QPalette()
    for role in [QPalette.Window, QPalette.Base, QPalette.AlternateBase]:
        palette.setColor(role, QColor("#2b2b2b"))
    for role in [QPalette.Text, QPalette.WindowText, QPalette.ButtonText]:
        palette.setColor(role, Qt.white)
    palette.setColor(QPalette.Button, QColor("#57a1a7"))
    app.setPalette(palette)
    
    window = ImgurUploader()
    window.show()
    sys.exit(app.exec_()) 