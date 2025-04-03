document.addEventListener("DOMContentLoaded", function () {
    const header = document.querySelector("#header");

    function updateHeader() {
        if (window.scrollY > 10) { 
            header.classList.add("header-scrolled");
        } else {
            header.classList.remove("header-scrolled");
        }
    }

    window.addEventListener("scroll", updateHeader);
    updateHeader(); // Вызываем сразу, чтобы учесть начальное положение

    // Модальное окно
    const modal = document.getElementById("bookingModal");
    const openModalBtn = document.querySelector(".book-button");
    const closeModal = document.getElementById("closeModal");

    openModalBtn.addEventListener("click", function (event) {
        event.preventDefault();
        modal.style.display = "flex";
    });

    closeModal.addEventListener("click", function () {
        modal.style.display = "none";
    });

    window.addEventListener("click", function (event) {
        if (event.target === modal) {
            modal.style.display = "none";
        }
    });
});
