import requests
import os

class BacklogAPIClient:
    def __init__(self, space_url, api_key):
        self.space_url = space_url.rstrip('/')
        self.api_key = api_key
        self.headers = {
            "Content-Type": "application/x-www-form-urlencoded"
        }

    # ------------------------
    # 課題取得・基本情報
    # ------------------------
    def get_projects(self):
        return self._get("/api/v2/projects", "プロジェクト取得")

    def get_priorities(self):
        return self._get("/api/v2/priorities", "優先度取得")

    def get_statuses(self):
        return self._get("/api/v2/statuses", "状態取得")

    def get_issue_types(self, project_id):
        return self._get(f"/api/v2/projects/{project_id}/issueTypes", "課題タイプ取得")

    def get_categories(self, project_id):
        return self._get(f"/api/v2/projects/{project_id}/categories", "カテゴリ取得")

    def get_users(self, project_id):
        return self._get(f"/api/v2/projects/{project_id}/users", "ユーザー取得")

    def get_versions(self, project_id):
        return self._get(f"/api/v2/projects/{project_id}/versions", "バージョン取得")

    def get_milestones(self, project_id):
        return self._get(f"/api/v2/projects/{project_id}/versions", "マイルストーン取得")


    def _get(self, endpoint, log_name="取得"):
        """
        GETリクエスト共通処理
        """
        url = f"{self.space_url}{endpoint}?apiKey={self.api_key}"

        try:
            response = requests.get(url)
            response.raise_for_status()

            print(f"✅ {log_name} 成功！")
            return response.json()
        except requests.RequestException as e:
            print(f"❌ {log_name} エラー: {e}")
            return None