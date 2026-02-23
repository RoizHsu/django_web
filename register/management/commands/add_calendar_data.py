from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from register.models import Calendar_Shift
from datetime import datetime, timedelta
from django.utils import timezone
import pytz


class Command(BaseCommand):
    help = '添加測試日曆班次數據'

    def add_arguments(self, parser):
        parser.add_argument(
            '--clear',
            action='store_true',
            help='清除所有現有的日曆數據',
        )

    def handle(self, *args, **options):
        if options['clear']:
            count = Calendar_Shift.objects.count()
            Calendar_Shift.objects.all().delete()
            self.stdout.write(
                self.style.WARNING(f'已清除 {count} 筆日曆數據')
            )

        # 確保至少有用戶
        users = User.objects.all()[:4]
        
        if not users.exists():
            self.stdout.write(
                self.style.ERROR('❌ 沒有找到用戶，請先創建用戶！')
            )
            self.stdout.write('提示: 使用 python manage.py createsuperuser 創建用戶')
            return
        
        # 獲取台北時區
        taipei_tz = pytz.timezone('Asia/Taipei')
        
        # 今天的日期（台北時區）
        now_taipei = datetime.now(taipei_tz)
        today = now_taipei.replace(hour=0, minute=0, second=0, microsecond=0)
        
        # 為每個用戶添加班次
        shifts_data = [
            {
                'title': '系統維護',
                'description': '定期系統維護與更新，確保系統穩定運行',
                'start_hour': 8,
                'end_hour': 12,
            },
            {
                'title': '客戶支援',
                'description': '處理客戶諮詢與技術支援',
                'start_hour': 9,
                'end_hour': 17,
            },
            {
                'title': '設備檢修',
                'description': '檢查並維修公司設備',
                'start_hour': 13,
                'end_hour': 18,
            },
            {
                'title': '值班待命',
                'description': '待命處理緊急事件與突發狀況',
                'start_hour': 10,
                'end_hour': 15,
            },
            {
                'title': '網路監控',
                'description': '監控網路狀態與安全',
                'start_hour': 14,
                'end_hour': 22,
            },
            {
                'title': '資料備份',
                'description': '執行系統資料備份作業',
                'start_hour': 6,
                'end_hour': 10,
            },
        ]
        
        created_count = 0
        skipped_count = 0
        
        self.stdout.write('\n開始添加測試數據...\n')
        
        for i, user in enumerate(users):
            shift_info = shifts_data[i % len(shifts_data)]
            
            # 檢查是否已經存在類似的班次
            start_time = today + timedelta(hours=shift_info['start_hour'])
            end_time = today + timedelta(hours=shift_info['end_hour'])
            
            existing = Calendar_Shift.objects.filter(
                user=user,
                title=shift_info['title'],
                start_time=start_time
            ).exists()
            
            if not existing:
                Calendar_Shift.objects.create(
                    user=user,
                    title=shift_info['title'],
                    description=shift_info['description'],
                    start_time=start_time,
                    end_time=end_time,
                    repair_user=user  # 設置發布人為自己
                )
                created_count += 1
                
                # 獲取用戶顯示名稱
                user_name = user.username
                if hasattr(user, 'profile') and user.profile.user_name:
                    user_name = user.profile.user_name
                
                self.stdout.write(
                    self.style.SUCCESS(
                        f'✓ 為 {user_name} 創建班次: {shift_info["title"]} '
                        f'({shift_info["start_hour"]:02d}:00 - {shift_info["end_hour"]:02d}:00)'
                    )
                )
            else:
                skipped_count += 1
        
        self.stdout.write('\n' + '='*60)
        self.stdout.write(
            self.style.SUCCESS(f'✓ 完成! 共創建 {created_count} 個班次記錄')
        )
        if skipped_count > 0:
            self.stdout.write(
                self.style.WARNING(f'• 跳過 {skipped_count} 個已存在的記錄')
            )
        self.stdout.write(
            self.style.SUCCESS(f'📊 目前總共有 {Calendar_Shift.objects.count()} 個班次記錄')
        )
        self.stdout.write('='*60 + '\n')
        
        # 提示如何查看
        self.stdout.write('查看方式:')
        self.stdout.write('  1. 訪問 http://localhost:8000/repair/')
        self.stdout.write('  2. 點擊「📅 日歷」標籤')
        self.stdout.write('  3. 或訪問管理後台: http://localhost:8000/admin/')
