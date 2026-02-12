document.addEventListener("DOMContentLoaded", function () {
    // Get the filter element
    const select = document.getElementById("filter");
    if (select) {
        const wrapper = select.parentElement;

        select.addEventListener("click", () => {
            wrapper.classList.toggle("open");
        });

        select.addEventListener("blur", () => {
            wrapper.classList.remove("open");
        });
    }

    // Get the list element
    const list = document.getElementById("list");
    if (list) {
        const listWrapper = list.parentElement;

        list.addEventListener("click", () => {
            listWrapper.classList.toggle("open");
        });

        list.addEventListener("blur", () => {
            listWrapper.classList.remove("open");
        });
    }
});
