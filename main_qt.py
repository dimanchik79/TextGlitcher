import sys
import os
from datetime import datetime
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

# ==================== СЛОВАРЬ ПЕРЕВОДОВ ====================
LANG = {
    'window_title': {'ru': '📄 Сборщик текстовых файлов', 'en': '📄 Text File Collector'},
    'subtitle': {'ru': 'Перетащите файлы в зону ниже или используйте кнопки для выбора', 'en': 'Drag files to the area below or use buttons to select'},
    
    'drop_text': {'ru': 'Перетащите файлы\nсюда', 'en': 'Drag files\nhere'},
    'drop_good': {'ru': 'Отлично! Продолжайте\nили нажмите кнопки', 'en': 'Great! Continue\nor click buttons'},
    'drop_count': {'ru': 'файлов', 'en': 'files'},
    
    'btn_add_files': {'ru': '📂 Добавить файлы', 'en': '📂 Add Files'},
    'btn_add_folder': {'ru': '📁 Добавить папку', 'en': '📁 Add Folder'},
    'btn_clear_all': {'ru': '🗑 Очистить все', 'en': '🗑 Clear All'},
    'btn_copy': {'ru': '📋 Копировать', 'en': '📋 Copy'},
    'btn_download': {'ru': '⬇ Скачать', 'en': '⬇ Download'},
    'btn_clear': {'ru': '✕ Очистить', 'en': '✕ Clear'},
    
    'header_file_list': {'ru': '📁 Список файлов', 'en': '📁 File List'},
    'header_result': {'ru': '📋 Результат сборки', 'en': '📋 Result'},
    
    'stats_empty': {'ru': '📊 Файлов: 0 | 📝 Строк: 0 | 📏 Размер: 0 Б', 'en': '📊 Files: 0 | 📝 Lines: 0 | 📏 Size: 0 B'},
    'stats_format': {'ru': '📊 Файлов: {} | 📝 Строк: {} | 📏 Размер: {}', 'en': '📊 Files: {} | 📝 Lines: {} | 📏 Size: {}'},
    
    'info_select': {'ru': 'Выберите файл для просмотра информации', 'en': 'Select a file to view information'},
    'info_format': {'ru': '📄 {}\n📁 {}\n📏 {} | 📝 {} строк', 'en': '📄 {}\n📁 {}\n📏 {} | 📝 {} lines'},
    
    'status_ready': {'ru': 'Готов к работе', 'en': 'Ready to work'},
    'status_added': {'ru': '✅ Добавлено {} файлов', 'en': '✅ Added {} files'},
    'status_added_folder': {'ru': '✅ Добавлено {} файлов из папки', 'en': '✅ Added {} files from folder'},
    'status_removed': {'ru': '🗑 Удалено {} файлов', 'en': '🗑 Removed {} files'},
    'status_cleared': {'ru': '🗑 Все файлы удалены', 'en': '🗑 All files cleared'},
    'status_copied': {'ru': '✅ Скопировано в буфер обмена', 'en': '✅ Copied to clipboard'},
    'status_downloaded': {'ru': '✅ Файл сохранен: {}', 'en': '✅ File saved: {}'},
    'status_cleared_result': {'ru': '✕ Результат очищен', 'en': '✕ Result cleared'},
    
    'dialog_confirm_title': {'ru': 'Подтверждение', 'en': 'Confirm'},
    'dialog_confirm_text': {'ru': 'Удалить все {} файлов?', 'en': 'Delete all {} files?'},
    'dialog_error_title': {'ru': 'Ошибка', 'en': 'Error'},
    'dialog_error_no_data': {'ru': 'Нет данных для копирования', 'en': 'No data to copy'},
    'dialog_error_no_data_download': {'ru': 'Нет данных для скачивания', 'en': 'No data to download'},
    'dialog_error_format': {'ru': 'Формат {} не поддерживается', 'en': 'Format {} is not supported'},
    'dialog_error_read': {'ru': 'Не удалось прочитать файл', 'en': 'Failed to read file'},
    'dialog_error_save': {'ru': 'Не удалось сохранить файл: {}', 'en': 'Failed to save file: {}'},
    'dialog_success_copy': {'ru': 'Скопировано в буфер обмена', 'en': 'Copied to clipboard'},
    'dialog_success_save': {'ru': 'Файл сохранен', 'en': 'File saved'},
    
    'menu_remove': {'ru': '🗑 Удалить выбранные', 'en': '🗑 Remove selected'},
    'menu_clear': {'ru': '🗑 Очистить все', 'en': '🗑 Clear all'},
    'menu_root': {'ru': 'Корень', 'en': 'Root'},
    
    'filter_text': {'ru': 'Текстовые файлы (*.txt *.log *.csv *.json *.xml *.md *.py *.js *.html *.css *.ini *.cfg *.conf);;Все файлы (*.*)', 
                    'en': 'Text files (*.txt *.log *.csv *.json *.xml *.md *.py *.js *.html *.css *.ini *.cfg *.conf);;All files (*.*)'},
    'filter_save': {'ru': 'Текстовые файлы (*.txt)', 'en': 'Text files (*.txt)'},
    
    'size_b': {'ru': 'Б', 'en': 'B'},
    'size_kb': {'ru': 'КБ', 'en': 'KB'},
    'size_mb': {'ru': 'МБ', 'en': 'MB'},
    'size_gb': {'ru': 'ГБ', 'en': 'GB'},
}

class FileItem:
    """Класс для хранения информации о файле"""
    def __init__(self, path, name, content, size):
        self.path = path
        self.name = name
        self.content = content
        self.size = size
        
    def get_display_name(self):
        dir_name = os.path.dirname(self.path)
        if dir_name:
            last_folder = os.path.basename(dir_name)
            return f"{self.name}  📁{last_folder}"
        return self.name
    
    def get_folder(self):
        dir_name = os.path.dirname(self.path)
        if dir_name:
            return os.path.basename(dir_name)
        return ""

class DropZone(QWidget):
    """Виджет зоны приема файлов"""
    file_dropped = pyqtSignal(list)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAcceptDrops(True)
        self.is_hover = False
        self.files_count = 0
        self.init_ui()
        
    def init_ui(self):
        self.setFixedSize(250, 250)
        self.setMinimumSize(200, 200)
        
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignCenter)
        layout.setSpacing(10)
        
        self.icon_label = QLabel("📁")
        self.icon_label.setAlignment(Qt.AlignCenter)
        self.icon_label.setStyleSheet("""
            font-size: 80px;
            background: transparent;
        """)
        layout.addWidget(self.icon_label)
        
        self.text_label = QLabel()
        self.text_label.setAlignment(Qt.AlignCenter)
        self.text_label.setStyleSheet("""
            color: #8892b0;
            font-size: 14px;
            background: transparent;
        """)
        layout.addWidget(self.text_label)
        
        self.count_label = QLabel()
        self.count_label.setAlignment(Qt.AlignCenter)
        self.count_label.setStyleSheet("""
            color: #64ffda;
            font-size: 12px;
            background: transparent;
        """)
        layout.addWidget(self.count_label)
        
        self.update_style()
    
    def update_texts(self, lang_func):
        """Обновление текстов с переданной функцией перевода"""
        if self.files_count == 0:
            self.text_label.setText(lang_func('drop_text'))
            self.count_label.setText(f"0 {lang_func('drop_count')}")
        else:
            self.text_label.setText(lang_func('drop_good'))
            self.count_label.setText(f"{self.files_count} {lang_func('drop_count')}")
        
    def update_style(self):
        if self.is_hover:
            icon_size = "100px" if self.files_count > 0 else "80px"
            
            self.icon_label.setStyleSheet(f"""
                font-size: {icon_size};
                background: transparent;
            """)
            
            self.setStyleSheet(f"""
                QWidget {{
                    background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                        stop:0 rgba(26, 42, 74, 0.8), stop:1 rgba(26, 26, 46, 0.8));
                    border: 3px dashed #64ffda;
                    border-radius: 20px;
                    box-shadow: 0 0 30px rgba(100, 255, 218, 0.3);
                }}
            """)
        else:
            self.icon_label.setStyleSheet("""
                font-size: 80px;
                background: transparent;
            """)
            
            self.setStyleSheet("""
                QWidget {
                    background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                        stop:0 #16213e, stop:1 #1a1a2e);
                    border: 2px dashed #2a3a5a;
                    border-radius: 20px;
                }
            """)
    
    def update_count(self, count, lang_func):
        self.files_count = count
        self.update_texts(lang_func)
        self.update_style()
    
    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            self.is_hover = True
            self.update_style()
            event.accept()
        else:
            event.ignore()
    
    def dragLeaveEvent(self, event):
        self.is_hover = False
        self.update_style()
        event.accept()
    
    def dragMoveEvent(self, event):
        if event.mimeData().hasUrls():
            event.accept()
        else:
            event.ignore()
    
    def dropEvent(self, event):
        self.is_hover = False
        self.update_style()
        
        files = []
        for url in event.mimeData().urls():
            path = url.toLocalFile()
            if os.path.exists(path):
                files.append(path)
        
        if files:
            self.file_dropped.emit(files)
        event.accept()

class TextGlitcherApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.files = []
        self.dark_mode = True
        self.current_lang = 'ru'
        
        # Список папок для игнорирования
        self.ignore_folders = {
            # Python
            '__pycache__',
            '.venv',
            'venv',
            'env',
            '.env',
            '__pypackages__',
            '.mypy_cache',
            '.pytest_cache',
            '.tox',
            '.eggs',
            '*.egg-info',
            '.ruff_cache',
            '.coverage',
            'htmlcov',
            'dist',
            'build',
            
            # IDE
            '.idea',
            '.vscode',
            '.gigacode',
            
            # Git
            '.git',
            '.gitignore',
            
            # JavaScript/Node
            'node_modules',
            
            # Other
            '__MACOSX',
            '.DS_Store',
            'Thumbs.db',
        }
        
        self.init_ui()
        self.apply_styles()
        self.apply_theme()
        self.update_all_texts()
        
    def _(self, key, *args):
        """Метод для получения перевода"""
        text = LANG.get(key, {}).get(self.current_lang, key)
        if args:
            return text.format(*args)
        return text
        
    def init_ui(self):
        self.setWindowTitle(self._('window_title'))
        self.setGeometry(100, 50, 1200, 800)
        
        central = QWidget()
        self.setCentralWidget(central)
        main_layout = QVBoxLayout(central)
        main_layout.setSpacing(10)
        main_layout.setContentsMargins(15, 15, 15, 15)
        
        # ===== ВЕРХНЯЯ ПАНЕЛЬ =====
        top_panel = QWidget()
        top_panel.setObjectName("topPanel")
        top_layout = QVBoxLayout(top_panel)
        top_layout.setSpacing(5)
        
        title_layout = QHBoxLayout()
        title_label = QLabel("📄 Сборщик текстовых файлов")
        title_label.setObjectName("titleLabel")
        title_layout.addWidget(title_label)
        title_layout.addStretch()
        
        # Кнопки переключения языка
        self.lang_ru_btn = QPushButton("🇷🇺 RU")
        self.lang_ru_btn.setObjectName("langBtn")
        self.lang_ru_btn.setFixedSize(60, 30)
        self.lang_ru_btn.clicked.connect(lambda: self.set_language('ru'))
        
        self.lang_en_btn = QPushButton("🇬🇧 EN")
        self.lang_en_btn.setObjectName("langBtn")
        self.lang_en_btn.setFixedSize(60, 30)
        self.lang_en_btn.clicked.connect(lambda: self.set_language('en'))
        
        self.theme_btn = QPushButton("🌙")
        self.theme_btn.setFixedSize(35, 35)
        self.theme_btn.setObjectName("themeBtn")
        self.theme_btn.clicked.connect(self.toggle_theme)
        
        lang_layout = QHBoxLayout()
        lang_layout.addWidget(self.lang_ru_btn)
        lang_layout.addWidget(self.lang_en_btn)
        lang_layout.addWidget(self.theme_btn)
        title_layout.addLayout(lang_layout)
        
        top_layout.addLayout(title_layout)
        
        self.subtitle_label = QLabel()
        self.subtitle_label.setObjectName("subtitleLabel")
        top_layout.addWidget(self.subtitle_label)
        
        main_layout.addWidget(top_panel)
        
        # ===== ЗОНА ПРИЕМКИ ФАЙЛОВ =====
        drop_container = QWidget()
        drop_container.setObjectName("dropContainer")
        drop_layout = QVBoxLayout(drop_container)
        drop_layout.setAlignment(Qt.AlignCenter)
        
        self.drop_zone = DropZone(self)
        self.drop_zone.file_dropped.connect(self.handle_dropped_files)
        drop_layout.addWidget(self.drop_zone, alignment=Qt.AlignCenter)
        
        main_layout.addWidget(drop_container)
        
        # ===== ПАНЕЛЬ ИНСТРУМЕНТОВ =====
        toolbar = QWidget()
        toolbar.setObjectName("toolbar")
        toolbar_layout = QHBoxLayout(toolbar)
        toolbar_layout.setSpacing(10)
        
        self.add_files_btn = self.create_tool_button("", self.add_files)
        self.add_folder_btn = self.create_tool_button("", self.add_folder)
        self.clear_btn = self.create_tool_button("", self.clear_all, danger=True)
        
        toolbar_layout.addWidget(self.add_files_btn)
        toolbar_layout.addWidget(self.add_folder_btn)
        toolbar_layout.addWidget(self.clear_btn)
        toolbar_layout.addStretch()
        
        self.stats_label = QLabel()
        self.stats_label.setObjectName("statsLabel")
        toolbar_layout.addWidget(self.stats_label)
        
        main_layout.addWidget(toolbar)
        
        # ===== ОСНОВНОЙ СПЛИТТЕР =====
        splitter = QSplitter(Qt.Horizontal)
        splitter.setHandleWidth(3)
        
        # ---- ЛЕВАЯ ПАНЕЛЬ ----
        left_widget = QWidget()
        left_widget.setObjectName("leftPanel")
        left_layout = QVBoxLayout(left_widget)
        left_layout.setSpacing(8)
        
        list_header = QHBoxLayout()
        self.list_header_label = QLabel()
        self.list_header_label.setObjectName("listHeader")
        list_header.addWidget(self.list_header_label)
        list_header.addStretch()
        
        self.file_count_label = QLabel("0")
        self.file_count_label.setObjectName("fileCount")
        list_header.addWidget(self.file_count_label)
        
        left_layout.addLayout(list_header)
        
        self.file_list = QListWidget()
        self.file_list.setObjectName("fileList")
        self.file_list.setContextMenuPolicy(Qt.CustomContextMenu)
        self.file_list.customContextMenuRequested.connect(self.show_context_menu)
        self.file_list.itemDoubleClicked.connect(self.remove_selected)
        self.file_list.setSelectionMode(QListWidget.ExtendedSelection)
        
        left_layout.addWidget(self.file_list)
        
        self.file_info_label = QLabel()
        self.file_info_label.setObjectName("fileInfo")
        self.file_info_label.setWordWrap(True)
        self.file_info_label.setMaximumHeight(60)
        left_layout.addWidget(self.file_info_label)
        
        splitter.addWidget(left_widget)
        
        # ---- ПРАВАЯ ПАНЕЛЬ ----
        right_widget = QWidget()
        right_widget.setObjectName("rightPanel")
        right_layout = QVBoxLayout(right_widget)
        right_layout.setSpacing(8)
        
        result_header = QHBoxLayout()
        self.result_header_label = QLabel()
        self.result_header_label.setObjectName("resultHeader")
        result_header.addWidget(self.result_header_label)
        result_header.addStretch()
        
        self.copy_btn = self.create_action_button("", self.copy_result)
        self.download_btn = self.create_action_button("", self.download_result)
        self.clear_result_btn = self.create_action_button("", self.clear_result)
        
        result_header.addWidget(self.copy_btn)
        result_header.addWidget(self.download_btn)
        result_header.addWidget(self.clear_result_btn)
        
        right_layout.addLayout(result_header)
        
        self.result_text = QTextEdit()
        self.result_text.setObjectName("resultText")
        self.result_text.setReadOnly(True)
        self.result_text.setFont(QFont("Consolas", 11))
        
        right_layout.addWidget(self.result_text)
        
        self.result_info = QLabel("")
        self.result_info.setObjectName("resultInfo")
        right_layout.addWidget(self.result_info)
        
        splitter.addWidget(right_widget)
        splitter.setSizes([350, 850])
        
        main_layout.addWidget(splitter)
        
        # ===== СТАТУС БАР =====
        self.status_bar = QStatusBar()
        self.status_bar.setObjectName("statusBar")
        self.setStatusBar(self.status_bar)
        
        self.status_indicator = QLabel("●")
        self.status_indicator.setObjectName("statusIndicator")
        self.status_bar.addPermanentWidget(self.status_indicator)
        
        self.status_label = QLabel()
        self.status_label.setObjectName("statusLabel")
        self.status_bar.addPermanentWidget(self.status_label)
        
        clear_status = QPushButton("✕")
        clear_status.setFixedSize(20, 20)
        clear_status.setObjectName("clearStatus")
        clear_status.clicked.connect(lambda: self.set_status(self._('status_ready'), "success"))
        self.status_bar.addPermanentWidget(clear_status)
        
        self.file_list.itemSelectionChanged.connect(self.show_file_info)
        
        self.apply_styles()
        self.set_status(self._('status_ready'), "success")
    
    def set_language(self, lang):
        """Установка языка"""
        if lang in ['ru', 'en']:
            self.current_lang = lang
            self.update_all_texts()
            self.update_ui()
            self.drop_zone.update_count(len(self.files), self._)
            self.set_status(f"🌐 {'Русский' if lang == 'ru' else 'English'}", "info")
    
    def update_all_texts(self):
        """Обновление всех текстов"""
        self.setWindowTitle(self._('window_title'))
        self.subtitle_label.setText(self._('subtitle'))
        
        self.add_files_btn.setText(self._('btn_add_files'))
        self.add_folder_btn.setText(self._('btn_add_folder'))
        self.clear_btn.setText(self._('btn_clear_all'))
        
        self.list_header_label.setText(self._('header_file_list'))
        self.result_header_label.setText(self._('header_result'))
        
        self.copy_btn.setText(self._('btn_copy'))
        self.download_btn.setText(self._('btn_download'))
        self.clear_result_btn.setText(self._('btn_clear'))
        
        self.drop_zone.update_texts(self._)
    
    def create_tool_button(self, text, callback, danger=False):
        btn = QPushButton(text)
        btn.clicked.connect(callback)
        if danger:
            btn.setObjectName("dangerBtn")
        else:
            btn.setObjectName("toolBtn")
        return btn
    
    def create_action_button(self, text, callback):
        btn = QPushButton(text)
        btn.clicked.connect(callback)
        btn.setObjectName("actionBtn")
        return btn
    
    def handle_dropped_files(self, paths):
        added = 0
        for path in paths:
            if os.path.isfile(path):
                if self.load_file(path):
                    added += 1
            elif os.path.isdir(path):
                added += self.load_folder(path)
        
        if added > 0:
            self.update_ui()
            self.drop_zone.update_count(len(self.files), self._)
            self.set_status(self._('status_added', added), "success")
    
    def apply_styles(self):
        self.setStyleSheet("""
            QMainWindow {
                background-color: #1a1a2e;
            }
            
            QWidget#topPanel {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #16213e, stop:1 #1a1a2e);
                border-radius: 10px;
                padding: 10px;
            }
            
            QWidget#dropContainer {
                background: transparent;
                padding: 10px;
            }
            
            QLabel#titleLabel {
                color: #e0e0e0;
                font-size: 22px;
                font-weight: bold;
            }
            
            QLabel#subtitleLabel {
                color: #8892b0;
                font-size: 13px;
            }
            
            QPushButton#langBtn {
                background-color: #2a3a5a;
                color: #e0e0e0;
                border: none;
                border-radius: 4px;
                font-weight: bold;
            }
            
            QPushButton#langBtn:hover {
                background-color: #3a4a6a;
            }
            
            QWidget#toolbar {
                background-color: #16213e;
                border-radius: 8px;
                padding: 8px;
            }
            
            QPushButton#toolBtn {
                background-color: #2a3a5a;
                color: #e0e0e0;
                border: none;
                border-radius: 6px;
                padding: 8px 16px;
                font-weight: bold;
            }
            
            QPushButton#toolBtn:hover {
                background-color: #3a4a6a;
            }
            
            QPushButton#dangerBtn {
                background-color: #4a2a2a;
                color: #ff6b6b;
                border: none;
                border-radius: 6px;
                padding: 8px 16px;
                font-weight: bold;
            }
            
            QPushButton#dangerBtn:hover {
                background-color: #5a3a3a;
            }
            
            QPushButton#themeBtn {
                background-color: transparent;
                color: #e0e0e0;
                border: 1px solid #3a4a6a;
                border-radius: 17px;
                font-size: 16px;
            }
            
            QPushButton#themeBtn:hover {
                background-color: #2a3a5a;
            }
            
            QLabel#statsLabel {
                color: #8892b0;
                font-size: 12px;
            }
            
            QWidget#leftPanel {
                background-color: #16213e;
                border-radius: 10px;
                padding: 10px;
            }
            
            QWidget#rightPanel {
                background-color: #16213e;
                border-radius: 10px;
                padding: 10px;
            }
            
            QLabel#listHeader {
                color: #e0e0e0;
                font-size: 14px;
                font-weight: bold;
            }
            
            QLabel#fileCount {
                color: #64ffda;
                font-size: 14px;
                font-weight: bold;
                background-color: #1a2a4a;
                border-radius: 10px;
                padding: 2px 10px;
            }
            
            QListWidget#fileList {
                background-color: #1a1a2e;
                border: 1px solid #2a3a5a;
                border-radius: 6px;
                color: #e0e0e0;
                font-size: 12px;
                padding: 5px;
                outline: none;
            }
            
            QListWidget#fileList::item {
                padding: 8px;
                border-radius: 4px;
            }
            
            QListWidget#fileList::item:selected {
                background-color: #2a4a6a;
                color: #ffffff;
            }
            
            QListWidget#fileList::item:hover {
                background-color: #1a2a4a;
            }
            
            QLabel#fileInfo {
                color: #8892b0;
                font-size: 11px;
                background-color: #1a1a2e;
                border-radius: 4px;
                padding: 5px;
            }
            
            QLabel#resultHeader {
                color: #e0e0e0;
                font-size: 14px;
                font-weight: bold;
            }
            
            QPushButton#actionBtn {
                background-color: #2a3a5a;
                color: #e0e0e0;
                border: none;
                border-radius: 4px;
                padding: 6px 14px;
                font-size: 12px;
            }
            
            QPushButton#actionBtn:hover {
                background-color: #3a4a6a;
            }
            
            QTextEdit#resultText {
                background-color: #0d0d1a;
                color: #e0e0e0;
                border: 1px solid #2a3a5a;
                border-radius: 6px;
                font-family: Consolas;
                font-size: 12px;
                padding: 10px;
            }
            
            QLabel#resultInfo {
                color: #64ffda;
                font-size: 11px;
            }
            
            QStatusBar#statusBar {
                background-color: #16213e;
                color: #8892b0;
                border-radius: 8px;
                margin-top: 5px;
            }
            
            QLabel#statusIndicator {
                color: #64ffda;
                font-size: 16px;
            }
            
            QLabel#statusLabel {
                color: #e0e0e0;
                font-size: 12px;
                margin-left: 5px;
            }
            
            QPushButton#clearStatus {
                background-color: transparent;
                color: #8892b0;
                border: none;
                font-size: 12px;
            }
            
            QPushButton#clearStatus:hover {
                color: #ff6b6b;
            }
            
            QSplitter::handle {
                background-color: #2a3a5a;
                border-radius: 2px;
            }
            
            QSplitter::handle:hover {
                background-color: #4a6a8a;
            }
            
            QScrollBar:vertical {
                background: #1a1a2e;
                width: 10px;
                border-radius: 5px;
            }
            
            QScrollBar::handle:vertical {
                background: #2a3a5a;
                border-radius: 5px;
                min-height: 20px;
            }
            
            QScrollBar::handle:vertical:hover {
                background: #4a6a8a;
            }
            
            QScrollBar:horizontal {
                background: #1a1a2e;
                height: 10px;
                border-radius: 5px;
            }
            
            QScrollBar::handle:horizontal {
                background: #2a3a5a;
                border-radius: 5px;
                min-width: 20px;
            }
            
            QScrollBar::handle:horizontal:hover {
                background: #4a6a8a;
            }
            
            QMenu {
                background-color: #1a1a2e;
                color: #e0e0e0;
                border: 1px solid #2a3a5a;
                border-radius: 6px;
                padding: 5px;
            }
            
            QMenu::item {
                padding: 8px 30px;
                border-radius: 4px;
            }
            
            QMenu::item:selected {
                background-color: #2a4a6a;
            }
            
            QMenu::separator {
                height: 1px;
                background-color: #2a3a5a;
                margin: 5px 10px;
            }
        """)
    
    def apply_theme(self):
        if self.dark_mode:
            self.theme_btn.setText("🌙")
        else:
            self.theme_btn.setText("☀️")
    
    def toggle_theme(self):
        self.dark_mode = not self.dark_mode
        self.apply_theme()
        
        if self.dark_mode:
            self.apply_styles()
        else:
            self.setStyleSheet("""
                QMainWindow {
                    background-color: #f0f4f8;
                }
                QWidget#topPanel {
                    background-color: #ffffff;
                    border-radius: 10px;
                    padding: 10px;
                }
                QWidget#dropContainer {
                    background: transparent;
                }
                QLabel#titleLabel {
                    color: #1a2a3a;
                    font-size: 22px;
                    font-weight: bold;
                }
                QLabel#subtitleLabel {
                    color: #6b7a8a;
                    font-size: 13px;
                }
                QPushButton#langBtn {
                    background-color: #e8edf2;
                    color: #1a2a3a;
                    border: none;
                    border-radius: 4px;
                    font-weight: bold;
                }
                QPushButton#langBtn:hover {
                    background-color: #d5dce3;
                }
                QWidget#toolbar {
                    background-color: #ffffff;
                    border-radius: 8px;
                    padding: 8px;
                }
                QPushButton#toolBtn {
                    background-color: #e8edf2;
                    color: #1a2a3a;
                    border: none;
                    border-radius: 6px;
                    padding: 8px 16px;
                    font-weight: bold;
                }
                QPushButton#toolBtn:hover {
                    background-color: #d5dce3;
                }
                QPushButton#dangerBtn {
                    background-color: #fde8e8;
                    color: #e74c3c;
                    border: none;
                    border-radius: 6px;
                    padding: 8px 16px;
                    font-weight: bold;
                }
                QPushButton#dangerBtn:hover {
                    background-color: #f5d0d0;
                }
                QLabel#statsLabel {
                    color: #6b7a8a;
                    font-size: 12px;
                }
                QWidget#leftPanel {
                    background-color: #ffffff;
                    border-radius: 10px;
                    padding: 10px;
                }
                QWidget#rightPanel {
                    background-color: #ffffff;
                    border-radius: 10px;
                    padding: 10px;
                }
                QLabel#listHeader {
                    color: #1a2a3a;
                    font-size: 14px;
                    font-weight: bold;
                }
                QLabel#fileCount {
                    color: #4a90d9;
                    font-size: 14px;
                    font-weight: bold;
                    background-color: #e8f0fe;
                    border-radius: 10px;
                    padding: 2px 10px;
                }
                QListWidget#fileList {
                    background-color: #f8fafc;
                    border: 1px solid #dce3ea;
                    border-radius: 6px;
                    color: #1a2a3a;
                    font-size: 12px;
                    padding: 5px;
                }
                QListWidget#fileList::item:selected {
                    background-color: #4a90d9;
                    color: #ffffff;
                }
                QListWidget#fileList::item:hover {
                    background-color: #e8f0fe;
                }
                QLabel#fileInfo {
                    color: #6b7a8a;
                    font-size: 11px;
                    background-color: #f8fafc;
                    border-radius: 4px;
                    padding: 5px;
                }
                QLabel#resultHeader {
                    color: #1a2a3a;
                    font-size: 14px;
                    font-weight: bold;
                }
                QPushButton#actionBtn {
                    background-color: #e8edf2;
                    color: #1a2a3a;
                    border: none;
                    border-radius: 4px;
                    padding: 6px 14px;
                    font-size: 12px;
                }
                QPushButton#actionBtn:hover {
                    background-color: #d5dce3;
                }
                QTextEdit#resultText {
                    background-color: #f8fafc;
                    color: #1a2a3a;
                    border: 1px solid #dce3ea;
                    border-radius: 6px;
                    font-family: Consolas;
                    font-size: 12px;
                    padding: 10px;
                }
                QLabel#resultInfo {
                    color: #27ae60;
                    font-size: 11px;
                }
                QStatusBar#statusBar {
                    background-color: #ffffff;
                    color: #6b7a8a;
                    border-radius: 8px;
                    margin-top: 5px;
                }
                QLabel#statusIndicator {
                    color: #27ae60;
                    font-size: 16px;
                }
                QLabel#statusLabel {
                    color: #1a2a3a;
                    font-size: 12px;
                    margin-left: 5px;
                }
                QSplitter::handle {
                    background-color: #dce3ea;
                    border-radius: 2px;
                }
                QMenu {
                    background-color: #ffffff;
                    color: #1a2a3a;
                    border: 1px solid #dce3ea;
                    border-radius: 6px;
                    padding: 5px;
                }
                QMenu::item:selected {
                    background-color: #4a90d9;
                    color: #ffffff;
                }
                QMenu::separator {
                    height: 1px;
                    background-color: #dce3ea;
                    margin: 5px 10px;
                }
            """)
    
    # ===== ЗАГРУЗКА ФАЙЛОВ =====
    def add_files(self):
        files, _ = QFileDialog.getOpenFileNames(
            self,
            self._('btn_add_files'),
            "",
            self._('filter_text')
        )
        
        added = 0
        for file_path in files:
            if self.load_file(file_path):
                added += 1
        
        if added > 0:
            self.update_ui()
            self.drop_zone.update_count(len(self.files), self._)
            self.set_status(self._('status_added', added), "success")
    
    def add_folder(self):
        folder = QFileDialog.getExistingDirectory(
            self,
            self._('btn_add_folder')
        )
        
        if folder:
            added = self.load_folder(folder)
            if added > 0:
                self.update_ui()
                self.drop_zone.update_count(len(self.files), self._)
                self.set_status(self._('status_added_folder', added), "success")
    
    def load_folder(self, folder_path):
        """
        Загружает файлы из папки, игнорируя системные и временные папки
        
        Игнорируемые папки:
        - __pycache__, .venv, venv, env, .env - Python окружения
        - .gigacode, .idea, .vscode - IDE настройки
        - .git, .gitignore - Git репозитории
        - node_modules - Node.js зависимости
        - и другие служебные папки
        """
        added = 0
        
        for root, dirs, files in os.walk(folder_path):
            # Исключаем игнорируемые папки из обхода
            dirs[:] = [d for d in dirs 
                      if d not in self.ignore_folders 
                      and not d.startswith('.')]
            
            for file in files:
                # Проверяем расширение файла
                ext = os.path.splitext(file)[1].lower()
                supported = ['.txt', '.log', '.csv', '.json', '.xml', '.md', 
                            '.py', '.js', '.html', '.css', '.ini', '.cfg', '.conf']
                
                if ext in supported:
                    file_path = os.path.join(root, file)
                    if self.load_file(file_path):
                        added += 1
        
        return added
    
    def load_file(self, file_path):
        ext = os.path.splitext(file_path)[1].lower()
        supported = ['.txt', '.log', '.csv', '.json', '.xml', '.md', 
                    '.py', '.js', '.html', '.css', '.ini', '.cfg', '.conf']
        
        if ext not in supported:
            return False
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
        except UnicodeDecodeError:
            try:
                with open(file_path, 'r', encoding='cp1251') as f:
                    content = f.read()
            except:
                return False
        except:
            return False
        
        name = os.path.basename(file_path)
        size = os.path.getsize(file_path)
        
        name = self.get_unique_name(name)
        
        self.files.append(FileItem(file_path, name, content, size))
        return True
    
    def get_unique_name(self, base_name):
        names = [f.name for f in self.files]
        if base_name not in names:
            return base_name
        
        name, ext = os.path.splitext(base_name)
        counter = 1
        while True:
            new_name = f"{name} ({counter}){ext}"
            if new_name not in names:
                return new_name
            counter += 1
    
    # ===== УПРАВЛЕНИЕ ФАЙЛАМИ =====
    def remove_selected(self):
        selected = self.file_list.selectedItems()
        if not selected:
            return
        
        for item in selected:
            index = self.file_list.row(item)
            if 0 <= index < len(self.files):
                del self.files[index]
        
        self.update_ui()
        self.drop_zone.update_count(len(self.files), self._)
        self.set_status(self._('status_removed', len(selected)), "warning")
    
    def clear_all(self):
        if not self.files:
            return
        
        reply = QMessageBox.question(
            self,
            self._('dialog_confirm_title'),
            self._('dialog_confirm_text', len(self.files)),
            QMessageBox.Yes | QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            self.files = []
            self.update_ui()
            self.drop_zone.update_count(0, self._)
            self.set_status(self._('status_cleared'), "warning")
    
    def clear_result(self):
        self.result_text.clear()
        self.result_info.setText("")
        self.set_status(self._('status_cleared_result'), "info")
    
    def show_context_menu(self, pos):
        menu = QMenu()
        
        remove_action = menu.addAction(self._('menu_remove'))
        remove_action.triggered.connect(self.remove_selected)
        
        menu.addSeparator()
        
        clear_action = menu.addAction(self._('menu_clear'))
        clear_action.triggered.connect(self.clear_all)
        
        menu.addSeparator()
        
        if self.file_list.currentItem():
            index = self.file_list.currentRow()
            if 0 <= index < len(self.files):
                file = self.files[index]
                info_action = menu.addAction(f"📄 {file.name}")
                info_action.setEnabled(False)
                folder = file.get_folder()
                if folder:
                    menu.addAction(f"📁 {folder}")
                else:
                    menu.addAction(f"📁 {self._('menu_root')}")
        
        menu.exec_(self.file_list.mapToGlobal(pos))
    
    def show_file_info(self):
        current = self.file_list.currentRow()
        if 0 <= current < len(self.files):
            file = self.files[current]
            folder = file.get_folder()
            info = self._('info_format', 
                         file.name, 
                         folder if folder else self._('menu_root'),
                         self.format_size(file.size),
                         file.content.count('\n') + 1)
            self.file_info_label.setText(info)
        else:
            self.file_info_label.setText(self._('info_select'))
    
    # ===== ОБНОВЛЕНИЕ ИНТЕРФЕЙСА =====
    def update_ui(self):
        self.update_file_list()
        self.update_stats()
        self.update_result()
    
    def update_file_list(self):
        self.file_list.clear()
        for file in self.files:
            display_name = file.get_display_name()
            size_str = self.format_size(file.size)
            self.file_list.addItem(f"{display_name}  [{size_str}]")
        
        self.file_count_label.setText(str(len(self.files)))
    
    def update_stats(self):
        if not self.files:
            self.stats_label.setText(self._('stats_empty'))
            return
        
        total_files = len(self.files)
        total_lines = 0
        total_size = 0
        
        for file in self.files:
            total_size += file.size
            total_lines += file.content.count('\n') + 1
        
        self.stats_label.setText(
            self._('stats_format', total_files, total_lines, self.format_size(total_size))
        )
    
    def update_result(self):
        self.result_text.clear()
        
        if not self.files:
            self.result_info.setText("")
            return
        
        result = []
        total_lines = 0
        
        for i, file in enumerate(self.files):
            if i > 0:
                result.append("\n\n\n\n\n")
            
            full_path = file.path
            left_sep = "=" * 10
            right_sep = "=" * 10
            result.append(f"{left_sep} 📁 {full_path} {right_sep}\n")
            
            result.append(file.content)
            
            if not file.content.endswith('\n'):
                result.append('\n')
            
            total_lines += file.content.count('\n') + 1
        
        text = ''.join(result)
        self.result_text.setText(text)
        
        self.result_info.setText(
            self._('stats_format', len(self.files), total_lines, self.format_size(sum(f.size for f in self.files)))
        )
    
    # ===== ДЕЙСТВИЯ С РЕЗУЛЬТАТОМ =====
    def copy_result(self):
        text = self.result_text.toPlainText().strip()
        if not text:
            QMessageBox.warning(self, self._('dialog_error_title'), self._('dialog_error_no_data'))
            return
        
        clipboard = QApplication.clipboard()
        clipboard.setText(text)
        self.set_status(self._('status_copied'), "success")
    
    def download_result(self):
        text = self.result_text.toPlainText().strip()
        if not text:
            QMessageBox.warning(self, self._('dialog_error_title'), self._('dialog_error_no_data_download'))
            return
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        default_name = f"combined_{timestamp}.txt"
        
        file_path, _ = QFileDialog.getSaveFileName(
            self,
            self._('btn_download'),
            default_name,
            self._('filter_save')
        )
        
        if file_path:
            try:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(text)
                self.set_status(self._('status_downloaded', os.path.basename(file_path)), "success")
            except Exception as e:
                QMessageBox.warning(self, self._('dialog_error_title'), self._('dialog_error_save', str(e)))
    
    # ===== ВСПОМОГАТЕЛЬНЫЕ ФУНКЦИИ =====
    def format_size(self, bytes):
        if bytes < 1024:
            return f"{bytes} {self._('size_b')}"
        elif bytes < 1024 * 1024:
            return f"{bytes / 1024:.1f} {self._('size_kb')}"
        elif bytes < 1024 * 1024 * 1024:
            return f"{bytes / (1024 * 1024):.1f} {self._('size_mb')}"
        else:
            return f"{bytes / (1024 * 1024 * 1024):.1f} {self._('size_gb')}"
    
    def set_status(self, message, status_type="info"):
        self.status_label.setText(message)
        
        colors = {
            "success": "#64ffda",
            "warning": "#ffd93d",
            "error": "#ff6b6b",
            "info": "#4a90d9"
        }
        
        self.status_indicator.setStyleSheet(f"color: {colors.get(status_type, '#64ffda')};")
        
        QTimer.singleShot(5000, lambda: self.status_label.setText(self._('status_ready')))

def main():
    app = QApplication(sys.argv)
    
    font = QFont("Segoe UI", 10)
    app.setFont(font)
    
    window = TextGlitcherApp()
    window.show()
    
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()