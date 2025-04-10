// dots.js
document.addEventListener("DOMContentLoaded", () => {
  const dots = document.querySelectorAll(".dot");
  dots.forEach((dot, index) => {
    dot.addEventListener("click", () => {
      window.location.href = dot.dataset.href;
    });
  });
});
