// scanline.js
setInterval(() => {
  const scanline = document.querySelector(".scanline");
  if (scanline) {
    scanline.style.top = "0";
    scanline.style.transition = "none";
    requestAnimationFrame(() => {
      scanline.style.transition = "top 1.5s linear";
      scanline.style.top = "100%";
    });
  }
}, 3000);
