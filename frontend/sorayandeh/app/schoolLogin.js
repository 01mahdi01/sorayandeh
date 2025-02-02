// مدیریت ارسال فرم
const loginForm = document.getElementById("loginForm");
const errorMessage = document.getElementById("errorMessage");

loginForm.addEventListener("submit", function (e) {
  e.preventDefault(); // جلوگیری از ارسال پیش‌فرض فرم

  // گرفتن اطلاعات فرم
  const loginData = {
    postal_code: document.getElementById("postal_code").value,
    school_code_num: document.getElementById("school_code_num").value,
    password: document.getElementById("password").value,
  };

  // ارسال داده‌ها به بک‌اند
  fetch(`${BASE_URL}applicant/login_school/`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(loginData),
  })
    .then((response) => {
      if (response.ok) {
        return response.json();
      } else if (response.status === 401) {
        throw new Error("نام کاربری یا رمز عبور اشتباه است.");
      } else if (response.status === 400) {
        throw new Error("لطفاً همه فیلدها را به درستی پر کنید.");
      } else {
        throw new Error("خطایی در سرور رخ داده است.");
      }
    })
    .then((result) => {
      // ذخیره توکن‌ها در LocalStorage
      // const accessToken = result.token.access;
      // const refreshToken = result.token.refresh;

      // localStorage.setItem("accessToken", accessToken);
      // if (refreshToken) {
      //   localStorage.setItem("refreshToken", refreshToken);
      // }
      const accessToken = result.access;
      const refreshToken = result.refresh;

      localStorage.setItem("accessToken", accessToken);
      localStorage.setItem("refreshToken", refreshToken);
      alert("ورود موفقیت‌آمیز بود!");
      console.log("نتیجه:", result);

      // انتقال به صفحه home
      window.location.href = "home.html";
    })
    .catch((error) => {
      // نمایش پیام خطا
      errorMessage.textContent = error.message;
    });
});
