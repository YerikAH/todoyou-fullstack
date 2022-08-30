export default function menuMobile() {
  const $hamOpen = document.getElementById("hamOpen");
  const $hamClose = document.getElementById("hamClose");
  const $menuMobile = document.getElementById("menuMobile");
  $hamOpen.addEventListener("click", (e) => {
    e.target.style.display = "none";
    $hamClose.style.display = "block";
    $menuMobile.style.display = "block";
  });
  $hamClose.addEventListener("click", (e) => {
    e.target.style.display = "none";
    $hamOpen.style.display = "block";
    $menuMobile.style.display = "none";
  });
}
