import sqlite3

conn = sqlite3.connect('db.sqlite3')
cursor = conn.cursor()

# 刪除 repair_repairuser 表
cursor.execute("DROP TABLE IF EXISTS repair_repairuser")

conn.commit()
print("repair_repairuser 表已刪除")

# 驗證
cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name LIKE 'repair%'")
tables = cursor.fetchall()
print("\n現有的 repair 表：")
for table in tables:
    print(f"  - {table[0]}")

# 檢查 repair_repair 表結構
cursor.execute("PRAGMA table_info(repair_repair)")
columns = cursor.fetchall()
print("\nrepair_repair 表結構：")
for col in columns:
    print(f"  {col[1]} ({col[2]})")

conn.close()
