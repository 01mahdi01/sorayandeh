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

    // دریافت فایل‌های تصویر
    const imageFiles = document.getElementById("campaignImages").files;

    // اگر فایلی انتخاب شده باشد، آن‌ها را آپلود کنید
    if (imageFiles.length > 0) {
      uploadImages(imageFiles).then((imageUrls) => {
        // پس از آپلود تصاویر، آدرس آن‌ها را به داده‌ها اضافه کنید
        data.preview_image = imageUrls;

        // ارسال داده‌ها به سرور
        sendDataToServer(data);
      });
    } else {
      // اگر تصویری انتخاب نشده بود، داده‌ها را بدون تصاویر ارسال کنید
      data.preview_image = []; // هیچ تصویری آپلود نشده است
      sendDataToServer(data);
    }
  });

  // تابع برای آپلود تصاویر
  function uploadImages(files) {
    const formData = new FormData();

    // افزودن فایل‌ها به FormData
    for (let i = 0; i < files.length; i++) {
      formData.append("images", files[i]);
    }

    // ارسال فایل‌ها به سرور برای آپلود
    return fetch(`${BASE_URL}upload/images/`, {
      method: "POST",
      body: formData,
    })
      .then((response) => {
        if (!response.ok) {
          throw new Error("خطا در آپلود تصاویر");
        }
        return response.json();
      })
      .then((data) => {
        // آدرس تصاویر آپلود شده را برگردانید
        return data.imageUrls; // فرض کنید سرور یک آرایه از آدرس‌ها برمی‌گرداند
      })
      .catch((error) => {
        console.error("خطا در آپلود تصاویر:", error);
        alert("خطا در آپلود تصاویر. لطفاً دوباره تلاش کنید.");
        return [];
      });
  }

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
