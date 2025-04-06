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

});
