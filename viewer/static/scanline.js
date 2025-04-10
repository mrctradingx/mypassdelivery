document.addEventListener("DOMContentLoaded", () => {
  const line = document.querySelector(".scanline");
  if (!line) return;
  let pos = 0;
  let down = true;

  setInterval(() => {
    pos += down ? 2 : -2;
    line.style.top = pos + "px";
    if (pos >= 80 || pos <= 0) down = !down;
  }, 30);
});