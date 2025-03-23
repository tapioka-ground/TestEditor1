import os
import tempfile
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QTextEdit,
    QPushButton, QComboBox, QMessageBox
)
from PySide6.QtGui import QPixmap
from PySide6.QtCore import Qt
from src.backlog_api_client import BacklogAPIClient



class BacklogSubmit(QWidget):
    def __init__(self, app_manager, image_pixmap=None):
        super().__init__()
        self.app_manager = app_manager
        self.image_pixmap = image_pixmap

        # APIクライアント作成
        self.api_key = "1qiWdd0tOMcgabSopxSGembHpr5W9bc5lgR8PSkmi9k8iF6XUvkwEeKKHcDvIZ3Y"
        self.space_url = "https://test09898.backlog.com"
        self.api_client = BacklogAPIClient(self.space_url, self.api_key)

        self.init_ui()
        self.fetch_projects()

    def init_ui(self):
        self.setWindowTitle("--Backlog--")
        self.resize(600, 600)
        self.layout = QVBoxLayout(self)

        # 各UI部品
        self.project_combo = QComboBox()
        self.layout.addWidget(QLabel("プロジェクトを選択"))
        self.layout.addWidget(self.project_combo)
        self.project_combo.currentIndexChanged.connect(self.project_changed)

        self.issue_type_combo = QComboBox()
        self.layout.addWidget(QLabel("課題の種別"))
        self.layout.addWidget(self.issue_type_combo)

        self.title_input = QLineEdit()
        self.layout.addWidget(QLabel("件名"))
        self.layout.addWidget(self.title_input)

        self.description_input = QTextEdit()
        self.layout.addWidget(QLabel("課題の詳細"))
        self.layout.addWidget(self.description_input)

        # 画像プレビュー
        self.image_preview_box = QHBoxLayout()
        self.layout.addLayout(self.image_preview_box)
        self.add_image_preview()

        row1 = QHBoxLayout()
        row1.addWidget(QLabel("状態"))
        self.status_combo = QComboBox()
        row1.addWidget(self.status_combo)

        row1.addWidget(QLabel("担当者"))
        self.assignee_combo = QComboBox()
        row1.addWidget(self.assignee_combo)
        self.layout.addLayout(row1)

        row2 = QHBoxLayout()
        row2.addWidget(QLabel("優先度"))
        self.priority_combo = QComboBox()
        row2.addWidget(self.priority_combo)

        row2.addWidget(QLabel("マイルストーン"))
        self.milestone_combo = QComboBox()
        row2.addWidget(self.milestone_combo)
        self.layout.addLayout(row2)

        row3 = QHBoxLayout()
        row3.addWidget(QLabel("カテゴリ"))
        self.category_combo = QComboBox()
        row3.addWidget(self.category_combo)

        row3.addWidget(QLabel("発生バージョン"))
        self.version_combo = QComboBox()
        row3.addWidget(self.version_combo)
        self.layout.addLayout(row3)

        self.submit_button = QPushButton("課題を追加")
        self.submit_button.clicked.connect(self.send_project)
        self.layout.addWidget(self.submit_button)

    def add_image_preview(self):
        if self.image_pixmap:
            image_label = QLabel()
            scaled_pixmap = self.image_pixmap.scaled(100, 100, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            image_label.setPixmap(scaled_pixmap)
            self.image_preview_box.addWidget(image_label)
        else:
            spacer = QLabel("（画像なし）")
            spacer.setStyleSheet("color: #888888; font-size: 12px;")
            self.image_preview_box.addWidget(spacer)

    def project_changed(self):
        project_id = self.project_combo.currentData()
        if project_id:
            self.fetch_issue_types(project_id)
            self.fetch_categories(project_id)
            self.fetch_users(project_id)
            self.fetch_versions(project_id)
            self.fetch_milestones(project_id)

    def fetch_projects(self):
        projects = self.api_client.get_projects()
        if projects:
            for project in projects:
                self.project_combo.addItem(project['name'], project['id'])
            self.project_changed()
            self.fetch_statuses()
            self.fetch_priorities()
        else:
            QMessageBox.warning(self, "エラー", "プロジェクト一覧取得に失敗しました")

    def fetch_issue_types(self, project_id):
        self.issue_type_combo.clear()
        issue_types = self.api_client.get_issue_types(project_id)
        if issue_types:
            for issue_type in issue_types:
                self.issue_type_combo.addItem(issue_type['name'], issue_type['id'])

    def fetch_categories(self, project_id):
        self.category_combo.clear()
        categories = self.api_client.get_categories(project_id)
        if categories:
            for category in categories:
                self.category_combo.addItem(category['name'], category['id'])

    def fetch_users(self, project_id):
        self.assignee_combo.clear()
        users = self.api_client.get_users(project_id)
        if users:
            for user in users:
                self.assignee_combo.addItem(user['name'], user['id'])

    def fetch_versions(self, project_id):
        self.version_combo.clear()
        versions = self.api_client.get_versions(project_id)
        if versions:
            for version in versions:
                self.version_combo.addItem(version['name'], version['id'])

    def fetch_milestones(self, project_id):
        self.milestone_combo.clear()
        milestones = self.api_client.get_milestones(project_id)
        if milestones:
            for milestone in milestones:
                self.milestone_combo.addItem(milestone['name'], milestone['id'])

    def fetch_statuses(self):
        statuses = self.api_client.get_statuses()
        if statuses:
            for status in statuses:
                self.status_combo.addItem(status['name'], status['id'])

    def fetch_priorities(self):
        priorities = self.api_client.get_priorities()
        if priorities:
            for priority in priorities:
                self.priority_combo.addItem(priority['name'], priority['id'])



    def send_project(self,):
        print("ここで課題あげるよ！")