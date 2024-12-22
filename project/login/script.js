document
  .getElementById("login-form")
  .addEventListener("submit", function (event) {
    event.preventDefault(); // جلوگیری از ارسال فرم به صورت پیش‌فرض

    const email = document.getElementById("email").value;
    const password = document.getElementById("password").value;

    // ارسال درخواست با استفاده از Fetch API
    fetch("http://127.0.0.1:8000/users/login/", {
      method: "POST", // متد درخواست
      headers: {
        "Content-Type": "application/json", // نوع محتوا
      },
      body: JSON.stringify({
        email: email,
        password: password,
      }), // داده‌هایی که ارسال می‌شود
    })
      .then((response) => {
        if (!response.ok) {
          throw new Error("خطای ناشناخته");
        } else {
          return response.json();
        }
      })
      .then((data) => {
        if (data.success) {
          // در صورتی که ورود موفقیت‌آمیز باشد
          alert("ورود با موفقیت انجام شد");
          window.location.href = "/dashboard"; // هدایت به داشبورد یا صفحه دیگر
        } else {
          const errorMessage = document.getElementById("error-message");
          errorMessage.textContent = error.message;
          errorMessage.style.display = "block";
          // اگر ورود ناموفق باشد
          throw new Error(data.message || "خطای نامشخص");
        }
      })
      .catch((error) => {
        // نمایش پیام خطا
        const errorMessage = document.getElementById("error-message");
        errorMessage.textContent = error.message;
        errorMessage.style.display = "block";
      });
  });
