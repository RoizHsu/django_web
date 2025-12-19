import sqlite3

# 連接資料庫
conn = sqlite3.connect('db.sqlite3')
cursor = conn.cursor()

# 創建 repair_repairuser 表
cursor.execute("""
CREATE TABLE IF NOT EXISTS repair_repairuser (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(255) NOT NULL
)
""")

conn.commit()
print("repair_repairuser 表已創建")

# 驗證
cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='repair_repairuser'")
result = cursor.fetchone()
if result:
    print(f"✓ 確認表已存在: {result[0]}")
else:
    print("✗ 表創建失敗")

conn.close()
