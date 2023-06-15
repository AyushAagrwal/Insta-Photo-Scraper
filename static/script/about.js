window.addEventListener("DOMContentLoaded", () => {
  const sections = document.querySelectorAll("section");

  sections.forEach((section, index) => {
    if (index % 2 !== 0) {
      section.classList.add("fade-in");
    }
  });
});
