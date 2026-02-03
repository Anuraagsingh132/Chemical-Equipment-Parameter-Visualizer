from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, 
    QLineEdit, QPushButton, QMessageBox, QFrame
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont

from api_client import APIClient


class LoginWindow(QDialog):
    """Login window for the desktop application."""
    
    def __init__(self, api_client: APIClient):
        super().__init__()
        self.api_client = api_client
        self.is_login_mode = True
        self.setup_ui()
    
    def setup_ui(self):
        self.setWindowTitle("Chemical Equipment Visualizer - Login")
        self.setFixedSize(420, 520)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.Dialog)
        
        # Main layout
        layout = QVBoxLayout(self)
        layout.setContentsMargins(40, 40, 40, 40)
        layout.setSpacing(20)
        
        # Title
        title_label = QLabel("Chemical Equipment\nVisualizer")
        title_label.setAlignment(Qt.AlignCenter)
        title_font = QFont("Segoe UI", 20, QFont.Bold)
        title_label.setFont(title_font)
        title_label.setStyleSheet("color: white; margin-bottom: 10px;")
        layout.addWidget(title_label)
        
        # Subtitle
        self.subtitle_label = QLabel("Sign in to your account")
        self.subtitle_label.setAlignment(Qt.AlignCenter)
        self.subtitle_label.setStyleSheet("color: rgba(255, 255, 255, 0.6); font-size: 14px;")
        layout.addWidget(self.subtitle_label)
        
        layout.addSpacing(20)
        
        # Username
        username_label = QLabel("Username")
        username_label.setStyleSheet("color: rgba(255, 255, 255, 0.8); font-weight: 500;")
        layout.addWidget(username_label)
        
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Enter your username")
        layout.addWidget(self.username_input)
        
        # Email (for register mode)
        self.email_label = QLabel("Email")
        self.email_label.setStyleSheet("color: rgba(255, 255, 255, 0.8); font-weight: 500;")
        self.email_label.hide()
        layout.addWidget(self.email_label)
        
        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText("Enter your email")
        self.email_input.hide()
        layout.addWidget(self.email_input)
        
        # Password
        password_label = QLabel("Password")
        password_label.setStyleSheet("color: rgba(255, 255, 255, 0.8); font-weight: 500;")
        layout.addWidget(password_label)
        
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Enter your password")
        self.password_input.setEchoMode(QLineEdit.Password)
        layout.addWidget(self.password_input)
        
        layout.addSpacing(10)
        
        # Submit button
        self.submit_btn = QPushButton("Sign In")
        self.submit_btn.setCursor(Qt.PointingHandCursor)
        self.submit_btn.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #6366f1, stop:1 #8b5cf6);
                padding: 14px;
                font-size: 15px;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #818cf8, stop:1 #a78bfa);
            }
        """)
        self.submit_btn.clicked.connect(self.on_submit)
        layout.addWidget(self.submit_btn)
        
        layout.addStretch()
        
        # Toggle mode
        toggle_layout = QHBoxLayout()
        toggle_layout.setAlignment(Qt.AlignCenter)
        
        self.toggle_label = QLabel("Don't have an account?")
        self.toggle_label.setStyleSheet("color: rgba(255, 255, 255, 0.6);")
        toggle_layout.addWidget(self.toggle_label)
        
        self.toggle_btn = QPushButton("Sign Up")
        self.toggle_btn.setCursor(Qt.PointingHandCursor)
        self.toggle_btn.setStyleSheet("""
            QPushButton {
                background: transparent;
                color: #818cf8;
                font-weight: bold;
                padding: 0;
            }
            QPushButton:hover {
                color: #a5b4fc;
            }
        """)
        self.toggle_btn.clicked.connect(self.toggle_mode)
        toggle_layout.addWidget(self.toggle_btn)
        
        layout.addLayout(toggle_layout)
        
        # Close button
        close_btn = QPushButton("✕")
        close_btn.setFixedSize(30, 30)
        close_btn.setCursor(Qt.PointingHandCursor)
        close_btn.setStyleSheet("""
            QPushButton {
                background: rgba(255, 255, 255, 0.1);
                border-radius: 15px;
                font-size: 14px;
            }
            QPushButton:hover {
                background: rgba(239, 68, 68, 0.3);
            }
        """)
        close_btn.clicked.connect(self.close)
        close_btn.move(375, 15)
        close_btn.setParent(self)
    
    def toggle_mode(self):
        self.is_login_mode = not self.is_login_mode
        
        if self.is_login_mode:
            self.subtitle_label.setText("Sign in to your account")
            self.submit_btn.setText("Sign In")
            self.toggle_label.setText("Don't have an account?")
            self.toggle_btn.setText("Sign Up")
            self.email_label.hide()
            self.email_input.hide()
        else:
            self.subtitle_label.setText("Create a new account")
            self.submit_btn.setText("Create Account")
            self.toggle_label.setText("Already have an account?")
            self.toggle_btn.setText("Sign In")
            self.email_label.show()
            self.email_input.show()
    
    def on_submit(self):
        username = self.username_input.text().strip()
        password = self.password_input.text().strip()
        email = self.email_input.text().strip()
        
        if not username or not password:
            QMessageBox.warning(self, "Error", "Username and password are required")
            return
        
        self.submit_btn.setEnabled(False)
        self.submit_btn.setText("Please wait...")
        
        try:
            if self.is_login_mode:
                self.api_client.login(username, password)
            else:
                self.api_client.register(username, password, email)
            
            # Open dashboard
            from dashboard_window import DashboardWindow
            self.dashboard = DashboardWindow(self.api_client)
            self.dashboard.show()
            self.close()
            
        except Exception as e:
            error_msg = str(e)
            if hasattr(e, 'response') and e.response is not None:
                try:
                    error_msg = e.response.json().get('error', str(e))
                except Exception:
                    pass
            QMessageBox.critical(self, "Error", f"Authentication failed: {error_msg}")
        
        finally:
            self.submit_btn.setEnabled(True)
            self.submit_btn.setText("Sign In" if self.is_login_mode else "Create Account")
    
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.drag_pos = event.globalPos() - self.frameGeometry().topLeft()
            event.accept()
    
    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.LeftButton and hasattr(self, 'drag_pos'):
            self.move(event.globalPos() - self.drag_pos)
            event.accept()
