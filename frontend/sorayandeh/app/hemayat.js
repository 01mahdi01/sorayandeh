function setAmount(amount) {
  document.getElementById("donationAmount").value = amount;
  updateTotalAmount();
}

function toggleCompanyField(isVisible) {
  document.getElementById("companyField").style.display = isVisible
    ? "block"
    : "none";
}

function updateTotalAmount() {
  const amount = document.getElementById("donationAmount").value || 0;
  document.getElementById("totalAmount").innerText =
    parseInt(amount).toLocaleString();
}

function submitDonation() {
  const amount = document.getElementById("donationAmount").value;
  if (!amount || amount <= 0) {
    alert("لطفاً مبلغی برای کمک وارد کنید.");
    return;
  }
  alert("از کمک شما سپاسگزاریم!");
}

// به‌روزرسانی مبلغ مجموع هنگام تغییر ورودی دستی
document
  .getElementById("donationAmount")
  .addEventListener("input", updateTotalAmount);
