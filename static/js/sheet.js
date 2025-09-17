$(function () {
  var today = new Date();//返回當前時間
  var yyyy = today.getFullYear();//獲取當前年份
  var MM = today.getMonth() +1;//因為gatMonth()方式獲取是索引值,所以要+1
  var dd = today.getDate();//返回一個月的某一天
  var hh = today.getHours();//返回小時(0-23)
  var mm = today.getMinutes();//返回分鐘
  MM = checkTime(MM);//調用下面的checkTime函數 設定小於10的時間格式
  dd = checkTime(dd);
  hh = checkTime(hh);
  mm = checkTime(mm);
  var time = yyyy+"-"+MM+"-"+dd+"T"+hh+":"+mm;
  var dateContorl = $("#currentDate");
  dateContorl.val(time);
  function  checkTime(i){
    if(i<10){
      i="0"+i;
    }
    return i ;
  }
});