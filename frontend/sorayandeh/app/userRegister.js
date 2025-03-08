const userRegistrationForm = document.getElementById("userRegistrationForm");
const errorMessagesDiv = document.getElementById("error-messages");
const errorList = document.getElementById("error-list");

// تابع برای اعتبارسنجی ایمیل
const validateEmail = (email) => {
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  return emailRegex.test(email);
};

// تابع برای اعتبارسنجی شماره تلفن (فرمت ایرانی)
const validatePhone = (phone) => {
  const phoneRegex = /^09[0-9]{9}$/;
  return phoneRegex.test(phone);
};

// تابع برای اعتبارسنجی رمز عبور
const validatePassword = (password) => {
  const passwordRegex =
    /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$/;
  return passwordRegex.test(password);
};

// تابع برای نمایش خطاها
const showError = (fieldId, errorMessage) => {
  const field = document.getElementById(fieldId);
  const errorElement = document.getElementById(`${fieldId}-error`);
  field.classList.add("is-invalid");
  errorElement.textContent = errorMessage;
};

// تابع برای پاک کردن خطاها
const clearErrors = () => {
  errorMessagesDiv.classList.add("d-none");
  errorList.innerHTML = "";
  document.querySelectorAll(".invalid-feedback").forEach((el) => {
    el.textContent = "";
    el.previousElementSibling.classList.remove("is-invalid");
  });
};

userRegistrationForm.addEventListener("submit", (e) => {
  e.preventDefault();
  clearErrors(); // پاک کردن خطاهای قبلی

  // دریافت مقادیر فیلدها
  const name = document.getElementById("name").value.trim();
  const email = document.getElementById("email").value.trim();
  const phone = document.getElementById("phone").value.trim();
  const password = document.getElementById("password").value.trim();
  const confirmPassword = document
    .getElementById("confirmPassword")
    .value.trim();
  const nationalCode = document.getElementById("nationalCode").value.trim();

  // اعتبارسنجی فیلدها
  let hasError = false;
  const errors = [];

  if (!name) {
    showError("name", "لطفاً نام و نام خانوادگی را وارد کنید.");
    errors.push("نام و نام خانوادگی را وارد کنید.");
    hasError = true;
  }

  if (!email) {
    showError("email", "لطفاً ایمیل را وارد کنید.");
    errors.push("ایمیل را وارد کنید.");
    hasError = true;
  } else if (!validateEmail(email)) {
    showError("email", "ایمیل نامعتبر است.");
    errors.push("ایمیل نامعتبر است.");
    hasError = true;
  }

  if (!phone) {
    showError("phone", "لطفاً شماره تلفن را وارد کنید.");
    errors.push("شماره تلفن را وارد کنید.");
    hasError = true;
  } else if (!validatePhone(phone)) {
    showError("phone", "شماره تلفن نامعتبر است.");
    errors.push("شماره تلفن نامعتبر است.");
    hasError = true;
  }

  if (!password) {
    showError("password", "لطفاً رمز عبور را وارد کنید.");
    errors.push("رمز عبور را وارد کنید.");
    hasError = true;
  } else if (!validatePassword(password)) {
    showError(
      "password",
      "رمز عبور باید حداقل ۸ کاراکتر، شامل حروف بزرگ، کوچک، عدد و علامت خاص باشد."
    );
    errors.push("رمز عبور نامعتبر است.");
    hasError = true;
  }

  if (!confirmPassword) {
    showError("confirmPassword", "لطفاً تایید رمز عبور را وارد کنید.");
    errors.push("تایید رمز عبور را وارد کنید.");
    hasError = true;
  } else if (password !== confirmPassword) {
    showError("confirmPassword", "رمز عبور و تایید رمز عبور مطابقت ندارند.");
    errors.push("رمز عبور و تایید رمز عبور مطابقت ندارند.");
    hasError = true;
  }

  // نمایش تمام خطاها در بخش خطاهای کلی
  if (hasError) {
    errorList.innerHTML = errors.map((err) => `<li>${err}</li>`).join("");
    errorMessagesDiv.classList.remove("d-none");
    return; // توقف ارسال فرم اگر خطایی وجود داشته باشد
  }

  // ارسال داده‌ها به سرور
  const data = {
    email: email,
    name: name,
    phone: phone,
    password: password,
    confirm_password: confirmPassword,
  };

  const info = {
    national_code: nationalCode,
  };

  const roll = "pe"; // برای کاربر عادی

  const mainJson = JSON.parse(JSON.stringify(data));
  const infoJson = JSON.parse(JSON.stringify(info));

  mainJson.info = infoJson;
  mainJson.roll = roll;

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

        window.location.href = "home.html"; // انتقال به صفحه اصلی
      } else if (status === 400) {
        const errorMessages = body.detail;
        let errors = [];

        // نمایش خطاهای مربوط به هر فیلد
        if (errorMessages.email) {
          showError("email", errorMessages.email.join(", "));
          errors.push(`ایمیل: ${errorMessages.email.join(", ")}`);
        }
        if (errorMessages.name) {
          showError("name", errorMessages.name.join(", "));
          errors.push(`نام: ${errorMessages.name.join(", ")}`);
        }
        if (errorMessages.phone) {
          showError("phone", errorMessages.phone.join(", "));
          errors.push(`شماره تلفن: ${errorMessages.phone.join(", ")}`);
        }
        if (errorMessages.password) {
          showError("password", errorMessages.password.join(", "));
          errors.push(`رمز عبور: ${errorMessages.password.join(", ")}`);
        }
        if (errorMessages.confirm_password) {
          showError(
            "confirmPassword",
            errorMessages.confirm_password.join(", ")
          );
          errors.push(
            `تایید رمز عبور: ${errorMessages.confirm_password.join(", ")}`
          );
        }
        if (errorMessages.national_code) {
          showError("nationalCode", errorMessages.national_code.join(", "));
          errors.push(`کد ملی: ${errorMessages.national_code.join(", ")}`);
        }

        // نمایش خطاها در بخش خطاهای کلی
        if (errors.length > 0) {
          errorList.innerHTML = errors.map((err) => `<li>${err}</li>`).join("");
          errorMessagesDiv.classList.remove("d-none");
        }
      } else {
        errorList.innerHTML =
          "<li>خطا در ثبت‌نام. لطفاً دوباره تلاش کنید.</li>";
        errorMessagesDiv.classList.remove("d-none");
        console.error("خطا در ثبت‌نام:", body);
      }
    })
    .catch((error) => {
      errorList.innerHTML =
        "<li>خطای شبکه یا مشکلی در ارسال داده‌ها رخ داده است.</li>";
      errorMessagesDiv.classList.remove("d-none");
      console.error("Error:", error);
    });
});

// مشاهده رمز
document.querySelectorAll(".toggle-password").forEach((item) => {
  item.addEventListener("click", function () {
    const targetId = this.getAttribute("data-target");
    const passwordField = document.getElementById(targetId);
    const icon = this.querySelector("i");

    if (passwordField.type === "password") {
      passwordField.type = "text";
      icon.classList.replace("bi-eye", "bi-eye-slash");
    } else {
      passwordField.type = "password";
      icon.classList.replace("bi-eye-slash", "bi-eye");
    }
  });
});
