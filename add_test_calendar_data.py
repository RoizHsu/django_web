"""
添加測試日曆數據
運行方式: python manage.py shell < add_test_calendar_data.py
或在 Django shell 中直接執行
"""

from django.contrib.auth.models import User
from register.models import Calendar_Shift
from datetime import datetime, timedelta
from django.utils import timezone
import pytz

def add_test_data():
    """添加測試日曆班次數據"""
    
    # 確保至少有一個用戶
    users = User.objects.all()[:4]
    
    if not users.exists():
        print("警告: 沒有找到用戶，請先創建用戶！")
        return
    
    # 清除舊的測試數據（可選）
    # Calendar_Shift.objects.all().delete()
    
    # 獲取台北時區
    taipei_tz = pytz.timezone('Asia/Taipei')
    
    # 今天的日期（台北時區）
    now_taipei = datetime.now(taipei_tz)
    today = now_taipei.replace(hour=0, minute=0, second=0, microsecond=0)
    
    # 為每個用戶添加班次
    shifts_data = [
        {
            'title': '系統維護',
            'description': '定期系統維護與更新',
            'start_hour': 8,
            'end_hour': 12,
            'color': '#4A90E2'
        },
        {
            'title': '客戶支援',
            'description': '處理客戶問題',
            'start_hour': 9,
            'end_hour': 17,
            'color': '#50C878'
        },
        {
            'title': '設備檢修',
            'description': '檢查並維修設備',
            'start_hour': 13,
            'end_hour': 18,
            'color': '#FF6B6B'
        },
        {
            'title': '值班待命',
            'description': '待命處理緊急事件',
            'start_hour': 10,
            'end_hour': 15,
            'color': '#FFD93D'
        },
    ]
    
    created_count = 0
    for i, user in enumerate(users):
        shift_info = shifts_data[i % len(shifts_data)]
        
        # 檢查是否已經存在類似的班次
        existing = Calendar_Shift.objects.filter(
            user=user,
            title=shift_info['title'],
            start_time=today + timedelta(hours=shift_info['start_hour'])
        ).exists()
        
        if not existing:
            Calendar_Shift.objects.create(
                user=user,
                title=shift_info['title'],
                description=shift_info['description'],
                start_time=today + timedelta(hours=shift_info['start_hour']),
                end_time=today + timedelta(hours=shift_info['end_hour']),
                repair_user=user  # 設置發布人為自己
            )
            created_count += 1
            print(f"✓ 為 {user.username} 創建班次: {shift_info['title']}")
        else:
            print(f"• 跳過 {user.username} 的 {shift_info['title']} (已存在)")
    
    print(f"\n完成! 共創建 {created_count} 個班次記錄")
    print(f"總共有 {Calendar_Shift.objects.count()} 個班次記錄")

# 執行函數
if __name__ == '__main__':
    add_test_data()
