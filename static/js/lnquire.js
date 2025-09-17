function sortTable() {
  var table, rows, switching, i, x, y, shouldSwitch;
  table = document.getElementById("myTable");
  switching = true;
  /* 设置一个循环语句 */
  while (switching) {
    // 设置循环结束标记
    switching = false;
    rows = table.rows;
    /* 循环表格的行 */
    for (i = 1; i < (rows.length - 1); i++) {
      // 设置元素是否调换位置
      shouldSwitch = false;
      /* 获取要比较的元素 */
      x = rows[i].getElementsByTagName("TD")[0];
      y = rows[i + 1].getElementsByTagName("TD")[0];
      // 判断是否将下一个元素与当前元素进行切换
      if (x.innerHTML.toLowerCase() > y.innerHTML.toLowerCase()) {
        // 设置调换元素标记，并结束当前循环
        shouldSwitch = true;
        break;
      }
    }
    if (shouldSwitch) {
      /* 如果元素调换位置设置为 true，则进行对调操作 */
      rows[i].parentNode.insertBefore(rows[i + 1], rows[i]);
      switching = true;
    }
  }
}