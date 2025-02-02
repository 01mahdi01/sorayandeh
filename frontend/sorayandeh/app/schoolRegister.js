const form = document.getElementById("registrationForm");

form.addEventListener("submit", function (e) {
  e.preventDefault(); // جلوگیری از ارسال پیش‌فرض فرم

  // گرفتن اطلاعات فرم و ساختاردهی داده‌ها
  const data = {
    name: document.getElementById("name").value,
    postal_code: document.getElementById("postal_code").value,
    school_code_num: document.getElementById("school_code_num").value,
    phone: document.getElementById("school_phone").value,
    email: document.getElementById("school_email").value,
    password: document.getElementById("password").value,
    address: document.getElementById("school_address").value,
  };

  // ساخت جیسون infoJson
  const infoJson = {
    employee_name: document.getElementById("employeeName").value,
    employee_phone: document.getElementById("employeePhone").value,
    employee_position: document.getElementById("employeePosition").value,
  };

  // ترکیب data و infoJson
  const mainJson = JSON.parse(JSON.stringify(data));
  const info = JSON.parse(JSON.stringify(infoJson));
  mainJson.creator_employee_info = infoJson;

  // ارسال داده‌ها با استفاده از fetch
  fetch(`${BASE_URL}applicant/register/`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(mainJson), // ارسال داده نهایی
  })
    .then((response) => {
      console.log(JSON.stringify(mainJson));
      // بررسی وضعیت پاسخ
      if (response.status === 200) {
        return response.json().then((result) => {
          alert("ثبت‌نام با موفقیت انجام شد!");
          console.log("پاسخ سرور:", result);

          window.location.href = "schoolLogin.html";
        });
      } else if (response.status === 400) {
        alert("درخواست نامعتبر است. لطفاً داده‌ها را بررسی کنید.");
      } else if (response.status === 401) {
        alert("خطای احراز هویت: شما دسترسی لازم را ندارید.");
      } else if (response.status === 403) {
        alert("دسترسی به این منبع ممنوع است.");
      } else if (response.status === 404) {
        alert("منبع مورد نظر یافت نشد.");
      } else if (response.status === 500) {
        alert("خطای سرور: مشکلی در سمت سرور رخ داده است.");
      } else {
        alert(`خطای ناشناخته رخ داده است (کد وضعیت: ${response.status}).`);
      }
    })
    .catch((error) => {
      // مدیریت خطاهای شبکه یا دیگر مشکلات
      alert("خطای شبکه یا مشکل دیگر رخ داده است.");
      console.error("Error:", error);
    });
});
