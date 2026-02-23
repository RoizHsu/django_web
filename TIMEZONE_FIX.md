# 🕐 時區問題修正說明

## 問題描述

Django 系統時間正確，但顯示到網頁的時間卻是錯誤的：
- **系統時區**: UTC+8 (台北時間)
- **資料庫儲存**: UTC+0 (UTC 時間)
- **顯示問題**: 時間差了 8 小時

## 原因分析

在 [settings.py](demo06/settings.py) 中設置：

```python
TIME_ZONE = 'Asia/Taipei'  # 台北時區 (UTC+8)
USE_TZ = True              # 啟用時區支持
```

當 `USE_TZ = True` 時：
1. Django 內部使用 **UTC 時間**儲存所有 datetime
2. 資料庫中的時間都是 **UTC+0**
3. 顯示時需要手動轉換到 **本地時區 (UTC+8)**

## 已修正的文件

### 1. [register/views.py](register/views.py)

**修正前**:
```python
start_hour = shift.start_time.hour  # 直接取 UTC 時間的小時
end_hour = shift.end_time.hour      # 結果會少 8 小時
```

**修正後**:
```python
# 轉換為台北時區
taipei_tz = pytz.timezone('Asia/Taipei')
start_time_taipei = shift.start_time.astimezone(taipei_tz)
end_time_taipei = shift.end_time.astimezone(taipei_tz)

# 提取台北時區的小時數
start_hour = start_time_taipei.hour  # 正確的台北時間
end_hour = end_time_taipei.hour
```

### 2. [register/management/commands/add_calendar_data.py](register/management/commands/add_calendar_data.py)

**修正前**:
```python
today = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
# 這會創建一個無時區感知的 datetime
```

**修正後**:
```python
taipei_tz = pytz.timezone('Asia/Taipei')
now_taipei = datetime.now(taipei_tz)
today = now_taipei.replace(hour=0, minute=0, second=0, microsecond=0)
# 創建時區感知的 datetime（台北時區）
```

### 3. [add_test_calendar_data.py](add_test_calendar_data.py)

同樣的修正，確保測試數據使用台北時區。

## 驗證步驟

### 1. 清除舊數據並重新創建

```bash
# 清除舊的測試數據
python manage.py add_calendar_data --clear

# 用正確時區重新添加
python manage.py add_calendar_data
```

### 2. 檢查 API 返回的時間

訪問: http://localhost:8000/register/api/calendar-shifts/

應該看到類似：
```json
{
  "success": true,
  "employees": [
    {
      "id": 1,
      "name": "張三",
      "shifts": [
        {
          "id": 1,
          "title": "系統維護",
          "start_hour": 8,      ← 應該是台北時間 8:00
          "end_hour": 12,       ← 應該是台北時間 12:00
          "start_time": "2026-02-13 08:00",  ← 台北時間
          "end_time": "2026-02-13 12:00"
        }
      ]
    }
  ]
}
```

### 3. 檢查數據庫中的實際儲存

在 Django shell 中：

```python
python manage.py shell

>>> from register.models import Calendar_Shift
>>> from django.utils import timezone
>>> import pytz

>>> shift = Calendar_Shift.objects.first()
>>> print(f"資料庫時間 (UTC): {shift.start_time}")
>>> # 輸出: 2026-02-13 00:00:00+00:00  (UTC)

>>> taipei_tz = pytz.timezone('Asia/Taipei')
>>> taipei_time = shift.start_time.astimezone(taipei_tz)
>>> print(f"台北時間: {taipei_time}")
>>> # 輸出: 2026-02-13 08:00:00+08:00  (台北時間)
```

## 時間轉換示例

| 項目 | UTC 時間 | 台北時間 (UTC+8) |
|------|----------|------------------|
| 早班開始 | 00:00 | 08:00 |
| 中班開始 | 05:00 | 13:00 |
| 晚班結束 | 14:00 | 22:00 |

## 重要概念

### Django 時區處理流程

```
用戶輸入時間 (台北時區)
    ↓
Django 轉換為 UTC
    ↓
儲存到資料庫 (UTC)
    ↓
從資料庫讀取 (UTC)
    ↓
轉換為台北時區 (.astimezone())
    ↓
顯示給用戶 (台北時區)
```

### 關鍵函數

1. **`astimezone(tz)`**: 轉換時區
   ```python
   taipei_time = utc_time.astimezone(pytz.timezone('Asia/Taipei'))
   ```

2. **`timezone.now()`**: 獲取當前時區感知的時間
   ```python
   from django.utils import timezone
   now = timezone.now()  # 返回 UTC 時間
   ```

3. **`timezone.localtime()`**: 轉換為本地時區
   ```python
   local_time = timezone.localtime(utc_time)
   ```

## 如果還有時間問題

### 檢查清單

- [ ] 確認 `settings.py` 中 `USE_TZ = True`
- [ ] 確認 `TIME_ZONE = 'Asia/Taipei'`
- [ ] 重新運行 `python manage.py add_calendar_data --clear`
- [ ] 檢查瀏覽器開發者工具 Console 是否有錯誤
- [ ] 清除瀏覽器緩存並重新載入頁面
- [ ] 檢查 API 返回的 JSON 數據
- [ ] 確認資料庫中有數據: `Calendar_Shift.objects.count()`

### 常見問題

**Q: 為什麼資料庫存的是 UTC 時間？**
A: 這是 Django 的最佳實踐，可以支持多時區用戶，避免夏令時問題。

**Q: 可以關閉 USE_TZ 嗎？**
A: 可以設為 `False`，但不建議。會失去時區支持，且未來移植困難。

**Q: 如何在模板中顯示正確時間？**
A: 使用 Django 模板過濾器：
```django
{{ shift.start_time|date:"Y-m-d H:i" }}
```
Django 會自動轉換為 `TIME_ZONE` 設置的時區。

## 參考資源

- [Django Time zones 文檔](https://docs.djangoproject.com/en/stable/topics/i18n/timezones/)
- [Python pytz 文檔](https://pythonhosted.org/pytz/)
- [時區轉換工具](https://www.timeanddate.com/worldclock/converter.html)

---

**修正完成時間**: 2026-02-13  
**影響範圍**: 日曆系統時間顯示  
**測試狀態**: ✅ 需要驗證
