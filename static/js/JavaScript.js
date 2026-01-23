document.addEventListener('DOMContentLoaded', () => {
// ========== 頁面切換功能 ==========
const navTabs = document.querySelectorAll('.nav-tab');
const pageContents = document.querySelectorAll('.page-content');

navTabs.forEach(tab => {
  tab.addEventListener('click', () => {
    const targetPage = tab.getAttribute('data-page');
    
    // 移除所有 active 狀態
    navTabs.forEach(t => t.classList.remove('active'));
    pageContents.forEach(p => p.classList.remove('active'));
    
    // 添加 active 狀態到當前選項
    tab.classList.add('active');
    document.getElementById(targetPage).classList.add('active');
  });
});

// ========== 浮動視窗功能 ==========
const openBtn = document.getElementById('openWinBtn');
const closeBtn = document.getElementById('closeWinBtn');
const minimizeBtn = document.querySelector('.minimize');
const maximizeBtn = document.querySelector('.maximize');
const win = document.getElementById('myWindow');
const header = win ? win.querySelector('.window-header') : null;
const resizer = win ? win.querySelector('.resizer') : null;

// 若元素未載入完成，略過初始化避免報錯
if (!openBtn || !closeBtn || !minimizeBtn || !maximizeBtn || !win || !header || !resizer) {
  console.warn('Window UI elements not found; skipping init.');
  return;
}

let isMaximized = false;
let prevDimensions = { width: 0, height: 0, top: 0, left: 0 };

// 打開視窗 (帶彈跳動畫)
openBtn.addEventListener('click', () => {
  win.style.display = 'flex';
  requestAnimationFrame(() => {
    win.classList.add('active');
  });
});

// 關閉視窗 (帶縮小動畫)
closeBtn.addEventListener('click', () => {
  win.classList.remove('active');
  setTimeout(() => {
    win.style.display = 'none';
    // 重置視窗狀態
    if (isMaximized) {
      isMaximized = false;
      restoreWindowSize();
    }
  }, 400);
});

// 最小化功能 (縮小到按鈕位置)
minimizeBtn.addEventListener('click', (e) => {
  e.stopPropagation();
  win.style.transition = 'transform 0.4s cubic-bezier(0.4, 0, 0.2, 1), opacity 0.3s';
  win.style.transform = 'translate(-50%, -50%) scale(0.1)';
  win.style.opacity = '0';
  
  setTimeout(() => {
    win.style.display = 'none';
    win.style.transform = 'translate(-50%, -50%) scale(0.8)';
    win.classList.remove('active');
  }, 400);
});

// 最大化/還原功能
maximizeBtn.addEventListener('click', (e) => {
  e.stopPropagation();
  
  if (!isMaximized) {
    // 保存當前尺寸
    prevDimensions.width = win.offsetWidth;
    prevDimensions.height = win.offsetHeight;
    prevDimensions.top = win.style.top;
    prevDimensions.left = win.style.left;
    
    // 最大化
    win.style.transition = 'all 0.3s cubic-bezier(0.4, 0, 0.2, 1)';
    win.style.width = '90vw';
    win.style.height = '90vh';
    win.style.top = '50%';
    win.style.left = '50%';
    win.style.transform = 'translate(-50%, -50%)';
    isMaximized = true;
  } else {
    // 還原
    restoreWindowSize();
  }
  
  setTimeout(() => {
    win.style.transition = '';
  }, 300);
});

function restoreWindowSize() {
  win.style.transition = 'all 0.3s cubic-bezier(0.4, 0, 0.2, 1)';
  win.style.width = prevDimensions.width + 'px';
  win.style.height = prevDimensions.height + 'px';
  win.style.top = prevDimensions.top || '50%';
  win.style.left = prevDimensions.left || '50%';
  isMaximized = false;
  
  setTimeout(() => {
    win.style.transition = '';
  }, 300);
}

// 拖拽功能 (改進版)
let isDragging = false;

header.addEventListener('mousedown', function(e) {
  if (isMaximized || e.target.classList.contains('control')) return;
  
  isDragging = true;
  win.classList.add('dragging');
  
  const rect = win.getBoundingClientRect();
  const shiftX = e.clientX - rect.left;
  const shiftY = e.clientY - rect.top;

  function moveAt(pageX, pageY) {
    win.style.left = pageX - shiftX + 'px';
    win.style.top = pageY - shiftY + 'px';
    win.style.transform = 'none';
  }

  function onMouseMove(e) {
    if (!isDragging) return;
    moveAt(e.pageX, e.pageY);
  }
  
  document.addEventListener('mousemove', onMouseMove);
  
  document.addEventListener('mouseup', function() {
    isDragging = false;
    win.classList.remove('dragging');
    document.removeEventListener('mousemove', onMouseMove);
  }, { once: true });
});

// 防止文字選取
header.addEventListener('dragstart', () => false);

// 縮放功能 (改進版)
let isResizing = false;

resizer.addEventListener('mousedown', function(e) {
  if (isMaximized) return;
  
  e.preventDefault();
  e.stopPropagation();
  isResizing = true;
  win.classList.add('resizing');
  
  const startX = e.clientX;
  const startY = e.clientY;
  const startWidth = win.offsetWidth;
  const startHeight = win.offsetHeight;

  function resize(e) {
    if (!isResizing) return;
    
    const newWidth = startWidth + (e.clientX - startX);
    const newHeight = startHeight + (e.clientY - startY);
    
    // 設定最小尺寸
    if (newWidth >= 300) {
      win.style.width = newWidth + 'px';
    }
    if (newHeight >= 200) {
      win.style.height = newHeight + 'px';
    }
  }

  function stopResize() {
    isResizing = false;
    win.classList.remove('resizing');
    window.removeEventListener('mousemove', resize);
    window.removeEventListener('mouseup', stopResize);
  }

  window.addEventListener('mousemove', resize);
  window.addEventListener('mouseup', stopResize);
});

// 雙擊標題列最大化/還原
header.addEventListener('dblclick', (e) => {
  if (e.target === header || e.target === win.querySelector('.window-title')) {
    maximizeBtn.click();
  }
});

// 添加鍵盤快捷鍵支持 (Esc 關閉視窗)
document.addEventListener('keydown', (e) => {
  if (e.key === 'Escape' && win.classList.contains('active')) {
    closeBtn.click();
  }
});
});