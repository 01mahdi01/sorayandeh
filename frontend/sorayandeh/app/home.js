const decreaseButton = document.getElementById("decrease");
const increaseButton = document.getElementById("increase");
const amountInput = document.getElementById("amount");
const priceDisplay = document.getElementById("price");

function updatePrice() {
  const amount = parseInt(amountInput.value) || 0;
  priceDisplay.textContent = amount;
}

decreaseButton.addEventListener("click", () => {
  let amount = parseInt(amountInput.value) || 0;
  amount = Math.max(0, amount - 10000); // حداقل مبلغ صفر
  amountInput.value = amount;
  updatePrice();
});

increaseButton.addEventListener("click", () => {
  let amount = parseInt(amountInput.value) || 0;
  amount += 10000;
  amountInput.value = amount;
  updatePrice();
});

amountInput.addEventListener("input", updatePrice);

amountInput.addEventListener("input", () => {
  let amount = parseInt(amountInput.value) || 0;

  if (amount > 50000000) {
    amount = 50000000; // محدود کردن به ۵۰,۰۰۰,۰۰۰
  }
  amountInput.value = amount;
});
// مم
document.addEventListener("DOMContentLoaded", () => {
  const carousel = document.querySelector("#logoCarousel");
  const carouselInstance = new bootstrap.Carousel(carousel, {
    interval: 5000, // جابجایی خودکار هر 5 ثانیه
    wrap: true,
  });

  // تنظیم حرکت یکی یکی
  carousel.addEventListener("slide.bs.carousel", (e) => {
    const items = carousel.querySelectorAll(".carousel-item");
    items.forEach((item) => item.classList.remove("active"));
    if (e.direction === "left") {
      items[e.to].classList.add("active");
    }
  });
});
