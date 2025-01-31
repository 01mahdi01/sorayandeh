const authForm = document.getElementById("authForm");

// مدیریت ارسال فرم ورود
authForm.addEventListener("submit", (e) => {
  e.preventDefault();

  // جمع‌آوری داده‌ها
  const email = document.getElementById("email").value;
  const password = document.getElementById("password").value;

  // داده‌های ورود
  const requestData = {
    email: email,
    password: password,
  };

  // ارسال به سرور
  fetch("http://91.107.162.10:1064/users/login/", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(requestData),
  })
    .then((response) => {
      console.log("پاسخ سرور:", response); // لاگ کردن پاسخ سرور
      if (!response.ok) {
        return response.json().then((errorData) => {
          console.error("جزئیات خطا:", errorData); // نمایش جزئیات خطا
          throw new Error(errorData.message || "مشکلی در احراز هویت وجود دارد");
        });
      }
      return response.json();
    })
    .then((data) => {
      const r = data;
      console.log("داده‌های دریافتی:", r); // لاگ داده‌های دریافتی

      // بررسی مقادیر دریافتی
      if (data.access && data.refresh) {
        // ذخیره توکن‌ها در localStorage
        localStorage.setItem("accessToken", data.access);
        localStorage.setItem("refreshToken", data.refresh);

        alert("ورود موفقیت‌آمیز!");
        // انتقال به داشبورد
        window.location.href = "home2.html";
      } else {
        alert("ورود ناموفق! لطفاً دوباره تلاش کنید.");
      }
    })
    .catch((error) => {
      console.error("خطا در ورود:", error.message);
      alert("ایمیل یا رمز اشتباه است");
    });
});
