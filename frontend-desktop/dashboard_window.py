import os
from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QPushButton, QListWidget, QListWidgetItem, QTableWidget,
    QTableWidgetItem, QFileDialog, QMessageBox, QFrame,
    QSplitter, QGroupBox, QHeaderView
)
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from PyQt5.QtGui import QFont

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt

from api_client import APIClient


class DataLoadThread(QThread):
    """Thread for loading data from API."""
    finished = pyqtSignal(dict)
    error = pyqtSignal(str)
    
    def __init__(self, api_client: APIClient, dataset_id: int):
        super().__init__()
        self.api_client = api_client
        self.dataset_id = dataset_id
    
    def run(self):
        try:
            stats = self.api_client.get_dataset_stats(self.dataset_id)
            equipment = self.api_client.get_equipment(self.dataset_id)
            self.finished.emit({"stats": stats, "equipment": equipment})
        except Exception as e:
            self.error.emit(str(e))


class DashboardWindow(QMainWindow):
    """Main dashboard window."""
    
    def __init__(self, api_client: APIClient):
        super().__init__()
        self.api_client = api_client
        self.datasets = []
        self.selected_dataset = None
        self.setup_ui()
        self.load_datasets()
    
    def setup_ui(self):
        self.setWindowTitle("Chemical Equipment Visualizer")
        self.setMinimumSize(1200, 800)
        
        # Central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Main layout
        main_layout = QHBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # Sidebar
        sidebar = self.create_sidebar()
        main_layout.addWidget(sidebar)
        
        # Content area
        content = self.create_content_area()
        main_layout.addWidget(content, 1)
    
    def create_sidebar(self) -> QFrame:
        sidebar = QFrame()
        sidebar.setFixedWidth(300)
        sidebar.setStyleSheet("""
            QFrame {
                background-color: rgba(255, 255, 255, 0.03);
                border-right: 1px solid rgba(255, 255, 255, 0.1);
            }
        """)
        
        layout = QVBoxLayout(sidebar)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(20)
        
        # Logo/Title
        title = QLabel("Equipment Visualizer")
        title.setFont(QFont("Segoe UI", 14, QFont.Bold))
        title.setStyleSheet("color: white;")
        layout.addWidget(title)
        
        # Upload button
        upload_btn = QPushButton("📁  Upload CSV")
        upload_btn.setCursor(Qt.PointingHandCursor)
        upload_btn.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #6366f1, stop:1 #8b5cf6);
                padding: 14px;
                font-size: 14px;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #818cf8, stop:1 #a78bfa);
            }
        """)
        upload_btn.clicked.connect(self.on_upload)
        layout.addWidget(upload_btn)
        
        # Datasets list
        datasets_label = QLabel("RECENT DATASETS")
        datasets_label.setStyleSheet("color: rgba(255, 255, 255, 0.5); font-size: 11px; font-weight: bold;")
        layout.addWidget(datasets_label)
        
        self.datasets_list = QListWidget()
        self.datasets_list.itemClicked.connect(self.on_dataset_selected)
        layout.addWidget(self.datasets_list, 1)
        
        # Logout button
        logout_btn = QPushButton("Logout")
        logout_btn.setCursor(Qt.PointingHandCursor)
        logout_btn.setStyleSheet("""
            QPushButton {
                background: rgba(239, 68, 68, 0.1);
                border: 1px solid rgba(239, 68, 68, 0.3);
                color: #f87171;
            }
            QPushButton:hover {
                background: rgba(239, 68, 68, 0.2);
            }
        """)
        logout_btn.clicked.connect(self.on_logout)
        layout.addWidget(logout_btn)
        
        return sidebar
    
    def create_content_area(self) -> QWidget:
        content = QWidget()
        layout = QVBoxLayout(content)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(20)
        
        # Header
        header_layout = QHBoxLayout()
        
        self.dataset_title = QLabel("Select a Dataset")
        self.dataset_title.setFont(QFont("Segoe UI", 20, QFont.Bold))
        self.dataset_title.setStyleSheet("color: white;")
        header_layout.addWidget(self.dataset_title)
        
        header_layout.addStretch()
        
        self.download_btn = QPushButton("📄  Download PDF Report")
        self.download_btn.setCursor(Qt.PointingHandCursor)
        self.download_btn.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #059669, stop:1 #10b981);
                padding: 12px 20px;
                font-size: 13px;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #10b981, stop:1 #34d399);
            }
        """)
        self.download_btn.clicked.connect(self.on_download_report)
        self.download_btn.setEnabled(False)
        header_layout.addWidget(self.download_btn)
        
        layout.addLayout(header_layout)
        
        # Stats cards
        self.stats_widget = self.create_stats_cards()
        layout.addWidget(self.stats_widget)
        
        # Charts and Table
        splitter = QSplitter(Qt.Vertical)
        
        # Chart area
        chart_widget = QWidget()
        chart_layout = QHBoxLayout(chart_widget)
        chart_layout.setContentsMargins(0, 0, 0, 0)
        
        # Bar chart
        self.bar_figure = Figure(figsize=(6, 4), facecolor='#0f0f23')
        self.bar_canvas = FigureCanvas(self.bar_figure)
        chart_layout.addWidget(self.bar_canvas)
        
        # Pie chart
        self.pie_figure = Figure(figsize=(4, 4), facecolor='#0f0f23')
        self.pie_canvas = FigureCanvas(self.pie_figure)
        chart_layout.addWidget(self.pie_canvas)
        
        splitter.addWidget(chart_widget)
        
        # Data table
        table_group = QGroupBox("Equipment Data")
        table_layout = QVBoxLayout(table_group)
        
        self.data_table = QTableWidget()
        self.data_table.setColumnCount(5)
        self.data_table.setHorizontalHeaderLabels([
            "Name", "Type", "Flowrate", "Pressure", "Temperature"
        ])
        self.data_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.data_table.setAlternatingRowColors(True)
        table_layout.addWidget(self.data_table)
        
        splitter.addWidget(table_group)
        splitter.setSizes([400, 300])
        
        layout.addWidget(splitter, 1)
        
        return content
    
    def create_stats_cards(self) -> QWidget:
        widget = QWidget()
        layout = QHBoxLayout(widget)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(16)
        
        self.stat_labels = {}
        
        stats_config = [
            ("total", "Total Equipment", "#8b5cf6"),
            ("flowrate", "Avg Flowrate", "#3b82f6"),
            ("pressure", "Avg Pressure", "#10b981"),
            ("temperature", "Avg Temperature", "#f59e0b"),
        ]
        
        for key, title, color in stats_config:
            card = QFrame()
            card.setStyleSheet(f"""
                QFrame {{
                    background-color: rgba(255, 255, 255, 0.05);
                    border-radius: 12px;
                    border: 1px solid rgba(255, 255, 255, 0.1);
                }}
            """)
            
            card_layout = QVBoxLayout(card)
            card_layout.setContentsMargins(20, 20, 20, 20)
            
            label = QLabel(title.upper())
            label.setStyleSheet("color: rgba(255, 255, 255, 0.5); font-size: 11px; font-weight: bold;")
            card_layout.addWidget(label)
            
            value_label = QLabel("--")
            value_label.setFont(QFont("Segoe UI", 24, QFont.Bold))
            value_label.setStyleSheet(f"color: {color};")
            card_layout.addWidget(value_label)
            
            self.stat_labels[key] = value_label
            layout.addWidget(card)
        
        return widget
    
    def load_datasets(self):
        try:
            self.datasets = self.api_client.list_datasets()
            self.datasets_list.clear()
            
            for dataset in self.datasets:
                item = QListWidgetItem(f"📊  {dataset['name']}")
                item.setData(Qt.UserRole, dataset)
                self.datasets_list.addItem(item)
            
            if self.datasets:
                self.datasets_list.setCurrentRow(0)
                self.on_dataset_selected(self.datasets_list.item(0))
                
        except Exception as e:
            QMessageBox.warning(self, "Error", f"Failed to load datasets: {e}")
    
    def on_dataset_selected(self, item: QListWidgetItem):
        dataset = item.data(Qt.UserRole)
        self.selected_dataset = dataset
        self.dataset_title.setText(dataset['name'])
        self.download_btn.setEnabled(True)
        
        # Load data in background
        self.load_thread = DataLoadThread(self.api_client, dataset['id'])
        self.load_thread.finished.connect(self.on_data_loaded)
        self.load_thread.error.connect(lambda e: QMessageBox.warning(self, "Error", e))
        self.load_thread.start()
    
    def on_data_loaded(self, data: dict):
        stats = data['stats']
        equipment = data['equipment']
        
        # Update stats cards
        self.stat_labels['total'].setText(str(stats.get('total_count', 0)))
        self.stat_labels['flowrate'].setText(f"{stats.get('avg_flowrate', 0):.2f}")
        self.stat_labels['pressure'].setText(f"{stats.get('avg_pressure', 0):.2f}")
        self.stat_labels['temperature'].setText(f"{stats.get('avg_temperature', 0):.2f}")
        
        # Update charts
        self.update_charts(stats.get('type_distribution', {}))
        
        # Update table
        self.update_table(equipment)
    
    def update_charts(self, distribution: dict):
        # Bar chart
        self.bar_figure.clear()
        ax = self.bar_figure.add_subplot(111)
        ax.set_facecolor('#0f0f23')
        
        if distribution:
            types = list(distribution.keys())
            counts = list(distribution.values())
            colors = ['#8b5cf6', '#6366f1', '#3b82f6', '#06b6d4', '#10b981', 
                      '#f59e0b', '#ef4444', '#ec4899', '#84cc16', '#14b8a6']
            
            bars = ax.bar(types, counts, color=colors[:len(types)])
            ax.set_ylabel('Count', color='white')
            ax.tick_params(axis='x', colors='white', rotation=45)
            ax.tick_params(axis='y', colors='white')
            ax.spines['bottom'].set_color((1, 1, 1, 0.2))
            ax.spines['left'].set_color((1, 1, 1, 0.2))
            ax.spines['top'].set_visible(False)
            ax.spines['right'].set_visible(False)
        
        self.bar_figure.tight_layout()
        self.bar_canvas.draw()
        
        # Pie chart
        self.pie_figure.clear()
        ax2 = self.pie_figure.add_subplot(111)
        ax2.set_facecolor('#0f0f23')
        
        if distribution:
            ax2.pie(counts, labels=types, autopct='%1.0f%%',
                    colors=colors[:len(types)], textprops={'color': 'white', 'fontsize': 9})
        
        self.pie_figure.tight_layout()
        self.pie_canvas.draw()
    
    def update_table(self, equipment: list):
        self.data_table.setRowCount(len(equipment))
        
        for row, item in enumerate(equipment):
            self.data_table.setItem(row, 0, QTableWidgetItem(item['name']))
            self.data_table.setItem(row, 1, QTableWidgetItem(item['equipment_type']))
            self.data_table.setItem(row, 2, QTableWidgetItem(f"{item['flowrate']:.2f}"))
            self.data_table.setItem(row, 3, QTableWidgetItem(f"{item['pressure']:.2f}"))
            self.data_table.setItem(row, 4, QTableWidgetItem(f"{item['temperature']:.2f}"))
    
    def on_upload(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Select CSV File", "", "CSV Files (*.csv)"
        )
        
        if file_path:
            try:
                self.api_client.upload_dataset(file_path)
                self.load_datasets()
                QMessageBox.information(self, "Success", "Dataset uploaded successfully!")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Upload failed: {e}")
    
    def on_download_report(self):
        if not self.selected_dataset:
            return
        
        save_path, _ = QFileDialog.getSaveFileName(
            self, "Save PDF Report", 
            f"{self.selected_dataset['name']}_report.pdf",
            "PDF Files (*.pdf)"
        )
        
        if save_path:
            try:
                self.api_client.download_report(self.selected_dataset['id'], save_path)
                QMessageBox.information(self, "Success", f"Report saved to {save_path}")
                os.startfile(save_path)
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Download failed: {e}")
    
    def on_logout(self):
        self.api_client.logout()
        from login_window import LoginWindow
        self.login_window = LoginWindow(self.api_client)
        self.login_window.show()
        self.close()
