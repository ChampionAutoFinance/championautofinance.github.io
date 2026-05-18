const creditButton = document.getElementById("creditApplication");
const notice = document.getElementById("notice");

let noticeTimer;

creditButton.addEventListener("click", () => {
  notice.classList.add("is-visible");

  window.clearTimeout(noticeTimer);
  noticeTimer = window.setTimeout(() => {
    notice.classList.remove("is-visible");
  }, 2200);
});
