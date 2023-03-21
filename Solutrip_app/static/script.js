let currentSlide = 0;

const slides = document.querySelectorAll("#slides img");
const prevBtn = document.querySelector("#prev");
const nextBtn = document.querySelector("#next");
const englishBtn = document.querySelector("#english");
const spanishBtn = document.querySelector("#spanish");
const content = document.querySelectorAll(".content");

englishBtn.addEventListener("click", () => {
  content.forEach((el) => {
    el.innerHTML = el.dataset.english;
  });
});

spanishBtn.addEventListener("click", () => {
  content.forEach((el) => {
    el.innerHTML = el.dataset.spanish;
  });
});

const showSlide = (n) => {
  currentSlide = (n + slides.length) % slides.length;
  slides.forEach((slide) => (slide.style.display = "none"));
  slides[currentSlide].style.display = "block";
};

prevBtn.addEventListener("click", () => showSlide(currentSlide - 1));
nextBtn.addEventListener("click", () => showSlide(currentSlide + 1));

showSlide(0);
