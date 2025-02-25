document.addEventListener("DOMContentLoaded", function () {
  const accessToken = localStorage.getItem("accessToken");

  // دریافت id کمپین از URL
  const urlParams = new URLSearchParams(window.location.search);
  const campaignId = urlParams.get("id");

  if (!campaignId) {
    console.error("Campaign ID not found in URL");
    return;
  }

  // تابع برای نمایش اطلاعات کمپین
  function displayCampaignDetails(campaign) {
    const detailsContainer = document.getElementById("campaign-details");

    const firstImage =
      campaign.gallery && campaign.gallery.length > 0
        ? `${BASE_URL}media/${campaign.gallery[0]}`
        : "image/placeholder.jpg"; // اگر عکسی وجود نداشت، از یک تصویر پیش‌فرض استفاده کنید

    const detailsHTML = `
        <div class="campaign-details">
          <img src="${firstImage}" class="campaign-image" alt="${
      campaign.title || "بدون عنوان"
    }" />
          <h1>${campaign.title || "بدون عنوان"}</h1>
          <p class="text-muted">دسته‌بندی: ${
            campaign.category || "بدون توضیحات"
          }</p>
          <p>${campaign.description}</p>
          <div class="progress">
            <div class="progress-bar" role="progressbar" style="width: 60%" aria-valuenow="60" aria-valuemin="0" aria-valuemax="100">
              <span>60%</span>
            </div>
          </div>
          <div class="amount-info mt-3">
            <p><strong>${campaign.steel_needed_money} از ${
      campaign.estimated_money
    } تومان</strong></p>
          </div>
        </div>
      `;

    detailsContainer.innerHTML = detailsHTML;
  }

  // ارسال درخواست به سرور برای دریافت اطلاعات کمپین
  fetch(`${BASE_URL}campaigns/single_campaign/`, {
    method: "POST", // استفاده از متد POST
    headers: {
      Authorization: `Bearer ${accessToken}`,
      "Content-Type": "application/json", // ارسال داده‌ها به صورت JSON
    },
    body: JSON.stringify({ id: campaignId }), // ارسال id کمپین در بدنه درخواست
  })
    .then((response) => {
      if (!response.ok) {
        throw new Error("Network response was not ok");
      }
      return response.json();
    })
    .then((data) => {
      console.log(data); // بررسی ساختار پاسخ سرور
      displayCampaignDetails(data); // نمایش اطلاعات کمپین
    })
    .catch((error) => {
      console.error("Error fetching campaign details:", error);
      const detailsContainer = document.getElementById("campaign-details");
      detailsContainer.innerHTML = "<p>خطا در دریافت اطلاعات کمپین.</p>";
    });
});
