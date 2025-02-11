const decreaseButton = document.getElementById("decrease");
const increaseButton = document.getElementById("increase");
const amountInput = document.getElementById("amount");
const priceDisplay = document.getElementById("price");

// تابع برای فرمت‌بندی عدد با کاما
function formatAmount(value) {
  return value.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
}

// تابع برای حذف کاماها و تبدیل مقدار به عدد صحیح
function cleanAmount(value) {
  return parseInt(value.replace(/,/g, "")) || 0;
}

// مقدار اولیه را فرمت کنید
amountInput.value = formatAmount(amountInput.value);

// تابع به‌روزرسانی مقدار ورودی و نمایش قیمت
function updateAmount(value) {
  if (value > 50000000) value = 50000000;
  if (value < 0) value = 0;

  amountInput.value = formatAmount(value);
  if (priceDisplay) priceDisplay.textContent = formatAmount(value);
}

// رویداد ورودی برای فرمت‌بندی در لحظه
amountInput.addEventListener("input", () => {
  updateAmount(cleanAmount(amountInput.value));
});

// دکمه کاهش مبلغ
decreaseButton.addEventListener("click", () => {
  updateAmount(cleanAmount(amountInput.value) - 10000);
});

// دکمه افزایش مبلغ
increaseButton.addEventListener("click", () => {
  updateAmount(cleanAmount(amountInput.value) + 10000);
});
