document
  .getElementById("registrationForm")
  .addEventListener("submit", function (event) {
    event.preventDefault(); // جلوگیری از ارسال فرم به صورت پیش‌فرض

    // گرفتن اطلاعات ورودی فرم
    const name = document.getElementById("name").value;
    const email = document.getElementById("email").value;
    const phone = document.getElementById("phone").value;
    const isLegal = document.getElementById("isLegal").value === "true"; // تغییر این قسمت به true/false
    const password = document.getElementById("password").value;
    const confirmPassword = document.getElementById("confirmPassword").value;
    const otp = document.getElementById("otp").value;

    const employeeName = document.getElementById("employee_name").value;
    const employeePosition = document.getElementById("employee_position").value;
    const companyRegistrationNumber = document.getElementById(
      "company_registration_number"
    ).value;

    // بررسی تطابق رمز عبور و تأیید آن
    if (password !== confirmPassword) {
      document.getElementById("responseMessage").textContent =
        "رمز عبور و تأیید آن یکسان نیستند.";
      document.getElementById("responseMessage").style.color = "red";
      return;
    }

    // ساختن شیء اطلاعات برای ارسال به سرور
    const userData = {
      email: email,
      name: name,
      phone: phone,
      is_company: isLegal,
      info: {
        employee_name: employeeName,
        employee_position: employeePosition,
        company_registration_number: companyRegistrationNumber,
      },
      password: password,
      confirm_password: confirmPassword,
    };

    // ارسال اطلاعات به سرور
    fetch("http://127.0.0.1:8000/users/register/", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(userData),
    })
      .then((response) => response.json())
      .then((data) => {
        // بررسی وضعیت پاسخ سرور
        if (data.success) {
          document.getElementById("responseMessage").textContent =
            "ثبت‌نام با موفقیت انجام شد!";
          document.getElementById("responseMessage").style.color = "green";
        } else {
          document.getElementById("responseMessage").textContent =
            "خطا در ثبت‌نام. لطفاً دوباره تلاش کنید.";
        }
      })
      .catch((error) => {
        document.getElementById("responseMessage").textContent =
          "خطا در ارتباط با سرور.";
        console.error("Error:", error);
      });
  });
