document.addEventListener("DOMContentLoaded", function () {
  const campaignForm = document.getElementById("campaignForm");

  campaignForm.addEventListener("submit", function (event) {
    event.preventDefault(); // جلوگیری از ارسال خودکار فرم

    // جمع‌آوری داده‌ها از فرم
    const data = {
      applicant_info: {
        firstName: document.getElementById("firstName").value,
        lastName: document.getElementById("lastName").value,
        position: document.getElementById("position").value,
        mobile: document.getElementById("mobile").value,
        schoolName: document.getElementById("schoolName").value,
        schoolPhone: document.getElementById("schoolPhone").value,
        schoolAddress: document.getElementById("schoolAddress").value,
      },
      category: document.getElementById("category").value,
      title: document.getElementById("campaignTitle").value,
      campaignDescription: document.getElementById("campaignDescription").value,
      estimated_money: document.getElementById("amount").value,
    };

    // ارسال داده‌ها به سرور
    sendDataToServer(data);
  });

  // تابع برای ارسال داده‌ها به سرور
  function sendDataToServer(data) {
    const accessToken = localStorage.getItem("accessToken"); // دریافت توکن دسترسی

    fetch(`${BASE_URL}campaigns/create/`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${accessToken}`, // افزودن توکن به هدر
      },
      body: JSON.stringify(data), // تبدیل داده‌ها به JSON
    })
      .then((response) => {
        if (!response.ok) {
          throw new Error("خطا در ارسال داده‌ها به سرور");
        }
        return response.json();
      })
      .then((responseData) => {
        console.log("کمپین با موفقیت ایجاد شد:", responseData);
        alert("کمپین با موفقیت ایجاد شد!");
        // هدایت کاربر به صفحه‌ی دیگر (اختیاری)
        window.location.href = "./campaigns.html";
      })
      .catch((error) => {
        console.error("خطا در ایجاد کمپین:", error);
        alert("خطا در ایجاد کمپین. لطفاً دوباره تلاش کنید.");
      });
  }
});
