// dots.js – hiệu ứng chuyển vé
const dots = document.createElement("div");
dots.style.position = "absolute";
dots.style.bottom = "20px";
dots.style.left = "50%";
dots.style.transform = "translateX(-50%)";
dots.style.display = "flex";
dots.style.gap = "6px";

const dotCount = 4; // tuỳ theo vé bạn có bao nhiêu
for (let i = 0; i < dotCount; i++) {
  const d = document.createElement("div");
  d.style.width = d.style.height = "10px";
  d.style.borderRadius = "50%";
  d.style.background = i === 0 ? "#000" : "#ccc";
  d.dataset.index = i;
  d.style.cursor = "pointer";
  dots.appendChild(d);
}
document.body.appendChild(dots);
