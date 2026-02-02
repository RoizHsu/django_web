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
const win = document.getElementById('myWindow');
const minimizeBtn = document.querySelector('.minimize');
const maximizeBtn = document.querySelector('.maximize');
const header = win ? win.querySelector('.window-header') : null;
const resizer = win ? win.querySelector('.resizer') : null;

// 修改視窗（已停用）
// const updateWinBtns = document.querySelectorAll('.updateWinBtn');
// const closeUpdateWinBtn = document.getElementById('closeUpdateWinBtn');
// const updateWin = document.getElementById('updateWindow');
// const minimizeUpdateWinBtn = updateWin ? updateWin.querySelector('.minimize') : null;
// const updateHeader = updateWin ? updateWin.querySelector('.window-header') : null;
// const updateResizer = updateWin ? updateWin.querySelector('.resizer') : null;

// 若視窗元素未載入完成，只略過視窗初始化，不要阻斷後續功能（例如表格分頁）
const hasWindowUI = openBtn && closeBtn && minimizeBtn && maximizeBtn && win && header && resizer;
// const hasUpdateWindowUI = updateWinBtns.length > 0 && closeUpdateWinBtn && updateWin && updateHeader;
if (!hasWindowUI) {
  console.warn('Window UI elements not found; skipping window init.');
}
// if (!hasUpdateWindowUI) {
//   console.warn('Update Window UI elements not found; skipping update window init.');
//   console.log('updateWinBtns.length:', updateWinBtns.length, 'closeUpdateWinBtn:', closeUpdateWinBtn, 'updateWin:', updateWin);
// }

if (hasWindowUI) {
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
}

// ========== 修改視窗功能（已停用） ==========
/*
if (hasUpdateWindowUI) {
  let isUpdateMaximized = false;
  let updatePrevDimensions = { width: 0, height: 0, top: 0, left: 0 };

  // 打開修改視窗
  updateWinBtns.forEach(btn => {
    btn.addEventListener('click', (e) => {
      e.preventDefault();
      e.stopPropagation();
      const repairId = btn.getAttribute('data-repair-id');
      console.log('打開修改視窗，維修單 ID:', repairId);
      updateWin.style.display = 'flex';
      requestAnimationFrame(() => {
        updateWin.classList.add('active');
      });
    });
  });

  // 關閉修改視窗
  closeUpdateWinBtn.addEventListener('click', () => {
    updateWin.classList.remove('active');
    setTimeout(() => {
      updateWin.style.display = 'none';
      // 重置視窗狀態
      if (isUpdateMaximized) {
        isUpdateMaximized = false;
        restoreUpdateWindowSize();
      }
    }, 400);
  });

  // 最小化功能 (縮小到按鈕位置)
  if (minimizeUpdateWinBtn) {
    minimizeUpdateWinBtn.addEventListener('click', (e) => {
      e.stopPropagation();
      updateWin.style.transition = 'transform 0.4s cubic-bezier(0.4, 0, 0.2, 1), opacity 0.3s';
      updateWin.style.transform = 'translate(-50%, -50%) scale(0.1)';
      updateWin.style.opacity = '0';
      
      setTimeout(() => {
        updateWin.style.display = 'none';
        updateWin.style.transform = 'translate(-50%, -50%) scale(0.8)';
        updateWin.classList.remove('active');
      }, 400);
    });
  }

  // 最大化/還原功能
  const maximizeUpdateBtn = updateWin ? updateWin.querySelector('.maximize') : null;
  if (maximizeUpdateBtn) {
    maximizeUpdateBtn.addEventListener('click', (e) => {
      e.stopPropagation();
      
      if (!isUpdateMaximized) {
        // 保存當前尺寸
        updatePrevDimensions.width = updateWin.offsetWidth;
        updatePrevDimensions.height = updateWin.offsetHeight;
        updatePrevDimensions.top = updateWin.style.top;
        updatePrevDimensions.left = updateWin.style.left;
        
        // 最大化
        updateWin.style.transition = 'all 0.3s cubic-bezier(0.4, 0, 0.2, 1)';
        updateWin.style.width = '90vw';
        updateWin.style.height = '90vh';
        updateWin.style.top = '50%';
        updateWin.style.left = '50%';
        updateWin.style.transform = 'translate(-50%, -50%)';
        isUpdateMaximized = true;
      } else {
        // 還原
        restoreUpdateWindowSize();
      }
      
      setTimeout(() => {
        updateWin.style.transition = '';
      }, 300);
    });
  }

  function restoreUpdateWindowSize() {
    updateWin.style.transition = 'all 0.3s cubic-bezier(0.4, 0, 0.2, 1)';
    updateWin.style.width = updatePrevDimensions.width + 'px';
    updateWin.style.height = updatePrevDimensions.height + 'px';
    updateWin.style.top = updatePrevDimensions.top || '50%';
    updateWin.style.left = updatePrevDimensions.left || '50%';
    isUpdateMaximized = false;
    
    setTimeout(() => {
      updateWin.style.transition = '';
    }, 300);
  }

  // 拖拽功能 (改進版)
  let isUpdateDragging = false;

  if (updateHeader) {
    updateHeader.addEventListener('mousedown', function(e) {
      if (isUpdateMaximized || e.target.classList.contains('control')) return;
      
      isUpdateDragging = true;
      updateWin.classList.add('dragging');
      
      const rect = updateWin.getBoundingClientRect();
      const shiftX = e.clientX - rect.left;
      const shiftY = e.clientY - rect.top;

      function moveAt(pageX, pageY) {
        updateWin.style.left = pageX - shiftX + 'px';
        updateWin.style.top = pageY - shiftY + 'px';
        updateWin.style.transform = 'none';
      }

      function onMouseMove(e) {
        if (!isUpdateDragging) return;
        moveAt(e.pageX, e.pageY);
      }
      
      document.addEventListener('mousemove', onMouseMove);
      
      document.addEventListener('mouseup', function() {
        isUpdateDragging = false;
        updateWin.classList.remove('dragging');
        document.removeEventListener('mousemove', onMouseMove);
      }, { once: true });
    });

    // 防止文字選取
    updateHeader.addEventListener('dragstart', () => false);

    // 雙擊標題列最大化/還原
    updateHeader.addEventListener('dblclick', (e) => {
      if (e.target === updateHeader || e.target === updateWin.querySelector('.window-title')) {
        if (maximizeUpdateBtn) {
          maximizeUpdateBtn.click();
        }
      }
    });
  }

  // 縮放功能 (改進版)
  let isUpdateResizing = false;

  if (updateResizer) {
    updateResizer.addEventListener('mousedown', function(e) {
      if (isUpdateMaximized) return;
      
      e.preventDefault();
      e.stopPropagation();
      isUpdateResizing = true;
      updateWin.classList.add('resizing');
      
      const startX = e.clientX;
      const startY = e.clientY;
      const startWidth = updateWin.offsetWidth;
      const startHeight = updateWin.offsetHeight;

      function resize(e) {
        if (!isUpdateResizing) return;
        
        const newWidth = startWidth + (e.clientX - startX);
        const newHeight = startHeight + (e.clientY - startY);
        
        // 設定最小尺寸
        if (newWidth >= 300) {
          updateWin.style.width = newWidth + 'px';
        }
        if (newHeight >= 200) {
          updateWin.style.height = newHeight + 'px';
        }
      }

      function stopResize() {
        isUpdateResizing = false;
        updateWin.classList.remove('resizing');
        window.removeEventListener('mousemove', resize);
        window.removeEventListener('mouseup', stopResize);
      }

      window.addEventListener('mousemove', resize);
      window.addEventListener('mouseup', stopResize);
    });
  }

  // 添加鍵盤快捷鍵支持 (Esc 關閉視窗)
  document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape' && updateWin.classList.contains('active')) {
      closeUpdateWinBtn.click();
    }
  });
}
*/


// ========== 表格分頁功能 ==========
const table = document.getElementById('DataTalbe');
const tbody = table ? table.querySelector('tbody') : null;
const rowsPerPage = 7;  // 每頁顯示行數（可自訂）
let currentPage = 1;

if (tbody) {
  const allRows = Array.from(tbody.querySelectorAll('tr'));
  const totalPages = Math.ceil(allRows.length / rowsPerPage);

  function showPage(pageNum) {
    const startIndex = (pageNum - 1) * rowsPerPage;
    const endIndex = startIndex + rowsPerPage;

    // 隱藏所有行
    allRows.forEach(row => row.style.display = 'none');

    // 顯示當前頁的行
    allRows.slice(startIndex, endIndex).forEach(row => row.style.display = '');

    // 更新頁碼顯示
    const pageInfo = document.getElementById('pageInfo');
    if (pageInfo) {
      pageInfo.textContent = `第 ${pageNum} 頁 / 共 ${totalPages} 頁`;
    }

    // 更新按鈕狀態
    const prevBtn = document.getElementById('prevPage');
    const nextBtn = document.getElementById('nextPage');
    if (prevBtn) prevBtn.disabled = pageNum === 1;
    if (nextBtn) nextBtn.disabled = pageNum === totalPages;
  }

  // 上一頁
  const prevBtn = document.getElementById('prevPage');
  if (prevBtn) {
    prevBtn.addEventListener('click', (e) => {
      e.preventDefault();
      e.stopPropagation();
      if (currentPage > 1) {
        currentPage--;
        showPage(currentPage);
      } else {
        alert('已經在第一頁了！');
      }
    });
  }

  // 下一頁
  const nextBtn = document.getElementById('nextPage');
  if (nextBtn) {
    nextBtn.addEventListener('click', (e) => {
      e.preventDefault();
      e.stopPropagation();
      if (currentPage < totalPages) {
        currentPage++;
        showPage(currentPage);
      } else {
        alert('已經到最後一頁了！');
      }
    });
  }

  // 初始化：顯示第一頁
  showPage(1);
}
});
