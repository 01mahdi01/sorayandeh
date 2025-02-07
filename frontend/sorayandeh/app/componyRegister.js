const companyRegistrationForm = document.getElementById(
  "companyRegistrationForm"
);

companyRegistrationForm.addEventListener("submit", (e) => {
  e.preventDefault();

  // داده‌های اصلی فرم
  const data = {
    email: document.getElementById("email").value,
    name: document.getElementById("name").value,
    phone: document.getElementById("phone").value,
    password: document.getElementById("password").value,
    confirm_password: document.getElementById("confirmPassword").value,
  };

  // داده‌های info به صورت جداگانه
  const info = {
    employee_name: document.getElementById("employeeName").value,
    employee_position: document.getElementById("employeePosition").value,
    company_registration_number:
      document.getElementById("companyRegNumber").value,
  };

  // اضافه کردن بخش roll
  const roll = "co"; // برای کمپانی

  // تبدیل داده‌ها به JSON
  const mainJson = JSON.parse(JSON.stringify(data));
  const infoJson = JSON.parse(JSON.stringify(info));

  mainJson.info = infoJson;
  mainJson.roll = roll;

  // ارسال داده به سمت بک‌اند
  fetch(`${BASE_URL}users/register/`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(mainJson),
  })
    .then((response) =>
      response
        .json()
        .then((result) => ({ status: response.status, body: result }))
    )
    .then(({ status, body }) => {
      if (status === 200 || status === 201) {
        const accessToken = body.token.access;
        const refreshToken = body.token.refresh;

        localStorage.setItem("accessToken", accessToken);
        if (refreshToken) {
          localStorage.setItem("refreshToken", refreshToken);
        }

        alert("ثبت‌نام با موفقیت انجام شد!");
        window.location.href = "home.html";
      } else if (status === 400) {
        const errorMessages = body.detail;
        if (errorMessages.email) {
          alert("خطا در ایمیل: " + errorMessages.email.join("\n"));
        }
        if (errorMessages.password) {
          alert("خطا در رمز عبور: " + errorMessages.password.join("\n"));
        }
        if (errorMessages.phone) {
          alert("خطا در شماره تلفن: " + errorMessages.phone.join("\n"));
        }
      }
    })
    .catch(() => {
      alert("خطای شبکه رخ داده است. لطفاً دوباره تلاش کنید.");
    });
});
// مشاهده رمط
document.querySelectorAll(".toggle-password").forEach((item) => {
  item.addEventListener("click", function () {
    const targetId = this.getAttribute("data-target");
    const passwordField = document.getElementById(targetId);
    const icon = this.querySelector("i");

    // تغییر نوع فیلد رمز عبور
    if (passwordField.type === "password") {
      passwordField.type = "text";
      icon.classList.replace("bi-eye", "bi-eye-slash"); // تغییر به آیکون چشم بسته
    } else {
      passwordField.type = "password";
      icon.classList.replace("bi-eye-slash", "bi-eye"); // تغییر به آیکون چشم باز
    }
  });
});
