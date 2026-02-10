const togglePassword = 
document.querySelector('#toggle-password');
//document.querySelector是用來選取HTML元素的方法（）搜尋函數
//參數是CSS選擇器字串，這裡選取id為toggle-password的元素
const password = 
document.querySelector('#password');
//document.querySelector是用來選取HTML元素的方法（）搜尋函數
//參數是CSS選擇器字串，這裡選取id為password的元素
if (togglePassword && password) {
    togglePassword.addEventListener('click',
        //為togglePassword元素添加點擊事件監聽器 user點擊按鈕時會觸發下列函數
        function () {
            //切換 type 屬性
            //把type屬性從 password 切換到 text 或反之
            const type = password.getAttribute('type') ===
            //getAttribute用來取得指定屬性的值 是來檢查目前的type屬性（輸入框是password還是text)
                'password' ? 'text' : 'password';
            password.setAttribute('type', type);
            //根據查到結果改成相應的type屬性（如：password會被改成text）
            //切換圖示
            //this.textContent = type === 'password' ? 
            //    '👁️' : '🙈';
            this.classList.toggle('fa-eye-slash');
        }
    );
}
