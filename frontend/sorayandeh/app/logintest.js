const accessToken = localStorage.getItem("accessToken");

// پیدا کردن عناصر HTML
const loginBtn = document.querySelector(".login-btn");
const loginBtnHum = document.querySelector(".login-btn-hum");
const menuLinks = document.querySelector(".menu-links");

// بررسی وجود توکن
if (accessToken) {
  fetch(`${BASE_URL}users/get_user/`, {
    method: "GET",
    headers: {
      "Content-Type": "application/json",
      Authorization: `Bearer ${accessToken}`,
    },
  })
    .then((response) => {
      if (!response.ok) {
        throw new Error("مشکلی در درخواست پیش آمد");
      }
      return response.json();
    })
    .then((data) => {
      // اطلاعات کاربر از پاسخ سرور
      const userInfo = data.json_data;
      console.log(userInfo);
      // نمایش نام کاربر و افزودن آیکون خروج
      loginBtn.innerHTML = `<i class="bi bi-person"></i> ${userInfo.name} 
  <i class="fa fa-sign-out fa-flip-horizontal logout-icon" style:"margin-right: 20px;"></i>`;
      loginBtnHum.innerHTML = `<a href="#">${userInfo.name}</a>`;

      // افزودن آیتم "پروفایل" و "خروج" به منوی همبرگری
      const profileItem = document.createElement("a");
      profileItem.href = "/BDC.html";
      profileItem.className = "menu-item profile-item";
      profileItem.innerHTML = `پروفایل <i class="bi bi-person-circle"></i> `;
      menuLinks.prepend(profileItem);

      const logoutItem = document.createElement("a");
      logoutItem.href = "/home.html";
      logoutItem.className = "menu-item logout-item";
      logoutItem.innerHTML = `<i class="fa fa-sign-out fa-flip-horizontal"></i> خروج`;
      menuLinks.appendChild(logoutItem);

      // اضافه کردن Event Listener برای دکمه خروج
      const logoutIcon = document.querySelector(".logout-icon");
      const logoutMenuItem = document.querySelector(".logout-item");

      const logoutHandler = () => {
        // حذف توکن‌ها از localStorage
        localStorage.removeItem("accessToken");
        localStorage.removeItem("refreshToken");

        // بازگرداندن دکمه‌های ورود
        loginBtn.innerHTML = `<a href="login.html">
    <i class="bi bi-person"></i>
    ورود | ثبت نام
  </a>`;
        loginBtnHum.innerHTML = `<a href="login.html">ورود و ثبت نام</a>`;

        // حذف آیتم‌های پروفایل و خروج از منوی همبرگری
        if (profileItem) profileItem.remove();
        if (logoutItem) logoutItem.remove();

        console.log("کاربر از سیستم خارج شد.");
      };

      logoutIcon.addEventListener("click", logoutHandler);
      logoutMenuItem.addEventListener("click", logoutHandler);
    })
    .catch((error) => {
      console.error("خطا در انجام درخواست:", error);
    });
} else {
  console.log("توکن دسترسی موجود نیست.");
}

// مدرسه
