# Django Web Application

用django創作前後端顯示畫面

## 專案簡介

這是一個使用 Django 6.0 框架建立的完整 Web 應用程式，展示了前後端整合的完整流程。專案包含了：

- ✅ Django 後端框架
- ✅ HTML 模板系統
- ✅ 靜態文件管理 (CSS/JavaScript)
- ✅ URL 路由配置
- ✅ 模板上下文傳遞
- ✅ 響應式網頁設計

## 功能特色

- **首頁 (Home)**: 展示專案特色和功能介紹
- **關於我們 (About)**: 專案詳細資訊和技術架構說明
- **聯絡我們 (Contact)**: 聯絡資訊展示和互動表單

## 技術架構

### 後端技術
- Django 6.0
- Python 3.12+
- SQLite 資料庫

### 前端技術
- HTML5
- CSS3 (響應式設計)
- JavaScript (ES6+)

## 安裝與執行

### 1. 克隆專案
```bash
git clone https://github.com/RoizHsu/django_web.git
cd django_web
```

### 2. 安裝依賴
```bash
pip install -r requirements.txt
```

### 3. 執行資料庫遷移
```bash
python manage.py migrate
```

### 4. 啟動開發伺服器
```bash
python manage.py runserver
```

### 5. 訪問應用程式
在瀏覽器中打開: `http://127.0.0.1:8000/`

## 專案結構

```
django_web/
├── manage.py              # Django 管理腳本
├── requirements.txt       # Python 依賴包
├── mysite/               # Django 專案設定目錄
│   ├── settings.py       # 專案設定
│   ├── urls.py          # 主要 URL 路由
│   └── wsgi.py          # WSGI 配置
├── main/                 # 主應用程式
│   ├── views.py         # 視圖函數
│   ├── urls.py          # 應用 URL 路由
│   ├── models.py        # 資料模型
│   └── templates/       # HTML 模板
│       └── main/
│           ├── base.html     # 基礎模板
│           ├── home.html     # 首頁模板
│           ├── about.html    # 關於頁面模板
│           └── contact.html  # 聯絡頁面模板
└── static/              # 靜態文件
    ├── css/
    │   └── style.css    # 樣式表
    └── js/
        └── main.js      # JavaScript 文件
```

## 開發說明

### 安全注意事項
⚠️ **重要**: 此專案使用開發環境設定，不適合直接部署到生產環境。在生產環境中應該：
- 使用環境變數設定 `SECRET_KEY`
- 將 `DEBUG` 設為 `False`
- 正確配置 `ALLOWED_HOSTS`
- 使用更安全的資料庫（如 PostgreSQL）

### 新增頁面
1. 在 `main/views.py` 中新增視圖函數
2. 在 `main/urls.py` 中新增 URL 路由
3. 在 `main/templates/main/` 中新增 HTML 模板

### 修改樣式
- 編輯 `static/css/style.css` 文件

### 新增 JavaScript 功能
- 編輯 `static/js/main.js` 文件

## 授權

© 2025 Django Web Application. All rights reserved.

## 作者

RoizHsu
