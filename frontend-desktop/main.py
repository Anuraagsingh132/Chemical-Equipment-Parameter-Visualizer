import sys
from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QFont, QPalette, QColor
from PyQt5.QtCore import Qt

from login_window import LoginWindow
from api_client import APIClient


def setup_dark_theme(app: QApplication):
    """Apply a modern dark theme to the application."""
    app.setStyle("Fusion")
    
    palette = QPalette()
    
    # Base colors
    palette.setColor(QPalette.Window, QColor(15, 15, 35))
    palette.setColor(QPalette.WindowText, QColor(255, 255, 255))
    palette.setColor(QPalette.Base, QColor(26, 26, 62))
    palette.setColor(QPalette.AlternateBase, QColor(35, 35, 75))
    palette.setColor(QPalette.ToolTipBase, QColor(255, 255, 255))
    palette.setColor(QPalette.ToolTipText, QColor(255, 255, 255))
    palette.setColor(QPalette.Text, QColor(255, 255, 255))
    palette.setColor(QPalette.Button, QColor(45, 45, 85))
    palette.setColor(QPalette.ButtonText, QColor(255, 255, 255))
    palette.setColor(QPalette.BrightText, QColor(255, 0, 0))
    palette.setColor(QPalette.Link, QColor(99, 102, 241))
    palette.setColor(QPalette.Highlight, QColor(99, 102, 241))
    palette.setColor(QPalette.HighlightedText, QColor(255, 255, 255))
    
    # Disabled colors
    palette.setColor(QPalette.Disabled, QPalette.Text, QColor(128, 128, 128))
    palette.setColor(QPalette.Disabled, QPalette.ButtonText, QColor(128, 128, 128))
    
    app.setPalette(palette)
    
    # Global stylesheet
    app.setStyleSheet("""
        QMainWindow, QDialog {
            background-color: #0f0f23;
        }
        
        QLabel {
            color: white;
        }
        
        QLineEdit {
            padding: 12px 16px;
            border: 1px solid rgba(255, 255, 255, 0.1);
            border-radius: 8px;
            background-color: rgba(255, 255, 255, 0.05);
            color: white;
            font-size: 14px;
        }
        
        QLineEdit:focus {
            border-color: #6366f1;
            background-color: rgba(99, 102, 241, 0.1);
        }
        
        QPushButton {
            padding: 12px 24px;
            border: none;
            border-radius: 8px;
            background-color: #6366f1;
            color: white;
            font-size: 14px;
            font-weight: bold;
        }
        
        QPushButton:hover {
            background-color: #818cf8;
        }
        
        QPushButton:pressed {
            background-color: #4f46e5;
        }
        
        QPushButton:disabled {
            background-color: #4a4a6a;
            color: #888;
        }
        
        QTableWidget {
            background-color: rgba(255, 255, 255, 0.05);
            border: 1px solid rgba(255, 255, 255, 0.1);
            border-radius: 8px;
            gridline-color: rgba(255, 255, 255, 0.05);
        }
        
        QTableWidget::item {
            padding: 8px;
            color: white;
        }
        
        QTableWidget::item:selected {
            background-color: rgba(99, 102, 241, 0.3);
        }
        
        QHeaderView::section {
            background-color: rgba(99, 102, 241, 0.2);
            color: white;
            padding: 12px;
            border: none;
            font-weight: bold;
        }
        
        QScrollBar:vertical {
            background: rgba(255, 255, 255, 0.05);
            width: 10px;
            border-radius: 5px;
        }
        
        QScrollBar::handle:vertical {
            background: rgba(255, 255, 255, 0.2);
            border-radius: 5px;
            min-height: 20px;
        }
        
        QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
            height: 0px;
        }
        
        QListWidget {
            background-color: transparent;
            border: none;
        }
        
        QListWidget::item {
            padding: 12px;
            border-radius: 8px;
            color: white;
            margin: 2px 0;
        }
        
        QListWidget::item:hover {
            background-color: rgba(255, 255, 255, 0.05);
        }
        
        QListWidget::item:selected {
            background-color: rgba(99, 102, 241, 0.2);
            border: 1px solid rgba(99, 102, 241, 0.5);
        }
        
        QGroupBox {
            font-weight: bold;
            border: 1px solid rgba(255, 255, 255, 0.1);
            border-radius: 8px;
            margin-top: 16px;
            padding-top: 16px;
            color: white;
        }
        
        QGroupBox::title {
            subcontrol-origin: margin;
            left: 16px;
            padding: 0 8px;
        }
    """)


def main():
    app = QApplication(sys.argv)
    
    # Set application info
    app.setApplicationName("Chemical Equipment Visualizer")
    app.setOrganizationName("FOSSEE")
    
    # Set font
    font = QFont("Segoe UI", 10)
    app.setFont(font)
    
    # Apply dark theme
    setup_dark_theme(app)
    
    # Create API client
    api_client = APIClient()
    
    # Show login window
    login_window = LoginWindow(api_client)
    login_window.show()
    
    sys.exit(app.exec_())


if __name__ == "__main__":
    # Enable High DPI scaling
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps)
    
    # Set Matplotlib to use Qt5 backend
    import matplotlib
    matplotlib.use("Qt5Agg")
    
    # Setup exception handling
    def exception_hook(exctype, value, traceback_obj):
        import traceback
        error_msg = "".join(traceback.format_exception(exctype, value, traceback_obj))
        print(error_msg)
        with open("crash_log.txt", "w") as f:
            f.write(error_msg)
            
        # Try to show error message if app is running
        try:
            from PyQt5.QtWidgets import QMessageBox
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText("Application Crashed")
            msg.setInformativeText(str(value))
            msg.setDetailedText(error_msg)
            msg.exec_()
        except:
            pass
            
        sys.exit(1)
        
    sys.excepthook = exception_hook
    
    main()
