document.addEventListener("DOMContentLoaded", function () {

    function setupToggle(elementId) {
        const element = document.getElementById(elementId);
        if (!element) return;

        const wrapper = element.parentElement;

        element.addEventListener("click", () => {
            wrapper.classList.toggle("open");
        });

        element.addEventListener("blur", () => {
            wrapper.classList.remove("open");
        });
    }

    setupToggle("filter");
});
