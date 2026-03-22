import os
import requests
import json
import time
from dotenv import load_dotenv

# .envファイルを読み込む
load_dotenv()

ACCESS_TOKEN = os.getenv("INSTAGRAM_ACCESS_TOKEN")
BUSINESS_ACCOUNT_ID = os.getenv("INSTAGRAM_BUSINESS_ACCOUNT_ID")

class InstaAnalyzer:
    def __init__(self):
        self.base_url = "https://graph.facebook.com/v22.0"
        self.data_dir = "../data/json"
        self.image_dir = "../data/images"

        if not os.path.exists(self.data_dir):
            os.makedirs(self.data_dir)
        if not os.path.exists(self.image_dir):
            os.makedirs(self.image_dir)

    def get_user_metadata(self, target_username):
        """指定したアカウントの基本情報を取得する (Business Discovery)"""
        url = f"{self.base_url}/{BUSINESS_ACCOUNT_ID}"
        params = {
            "fields": f"business_discovery.username({target_username}){{followers_count,media_count,name,biography,profile_picture_url}}",
            "access_token": ACCESS_TOKEN
        }
        response = requests.get(url, params=params)
        return response.json()

    def get_all_media_data(self, target_username):
        """指定したアカウントの全投稿データを取得する"""
        all_media = []
        url = f"{self.base_url}/{BUSINESS_ACCOUNT_ID}"
        
        # 取得したいフィールド
        # fields = "business_discovery.username(TARGET){media{id,caption,like_count,comments_count,media_url,timestamp,media_type,permalink}}"
        
        params = {
            "fields": f"business_discovery.username({target_username}){{media.limit(100){{id,caption,like_count,comments_count,media_url,timestamp,media_type,permalink}}}}",
            "access_token": ACCESS_TOKEN
        }

        print(f"[*] {target_username} のデータ取得を開始します...")
        
        while True:
            response = requests.get(url, params=params)
            res_json = response.json()

            if "error" in res_json:
                print(f"[!] エラーが発生しました: {res_json['error']['message']}")
                break

            media_data = res_json.get("business_discovery", {}).get("media", {})
            data_list = media_data.get("data", [])
            all_media.extend(data_list)
            print(f"[+] {len(all_media)} 件取得しました...")

            # ページネーション (次のデータがある場合)
            paging = media_data.get("paging", {})
            next_cursor = paging.get("cursors", {}).get("after")
            
            if next_cursor:
                params["fields"] = f"business_discovery.username({target_username}){{media.after({next_cursor}).limit(100){{id,caption,like_count,comments_count,media_url,timestamp,media_type,permalink}}}}"
                time.sleep(1) # Rate Limit回避
            else:
                break

        # JSONファイルとして保存
        file_path = f"{self.data_dir}/{target_username}_all_posts.json"
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(all_media, f, ensure_ascii=False, indent=4)
        
        print(f"[✓] {len(all_media)} 件の全投稿データを保存しました: {file_path}")
        return all_media

    def download_images(self, media_list, target_username):
        """メディア内の画像をローカルに保存する"""
        user_image_dir = f"{self.image_dir}/{target_username}"
        if not os.path.exists(user_image_dir):
            os.makedirs(user_image_dir)

        print(f"[*] 画像のダウンロードを開始します (保存先: {user_image_dir})...")
        for media in media_list:
            media_url = media.get("media_url")
            media_id = media.get("id")
            if not media_url:
                continue

            try:
                img_data = requests.get(media_url).content
                ext = "jpg" # デフォルト
                if "video" in media.get("media_type", "").lower():
                    ext = "mp4"
                
                with open(f"{user_image_dir}/{media_id}.{ext}", "wb") as f:
                    f.write(img_data)
            except Exception as e:
                print(f"[!] ID {media_id} の画像ダウンロードに失敗しました: {e}")

        print("[✓] 画像のダウンロードが完了しました。")

if __name__ == "__main__":
    # 使用例 (実行時はACCESS_TOKENが必要)
    # analyzer = InstaAnalyzer()
    # media = analyzer.get_all_media_data("nintendo_jp") # 例
    # analyzer.download_images(media, "nintendo_jp")
    pass
