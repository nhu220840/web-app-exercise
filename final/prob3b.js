document.addEventListener("DOMContentLoaded", () => {
    const form = document.getElementById("student-form");
    form.addEventListener("submit", function(event) {
        if (!validScore(event)) {
            event.preventDefault();
        }
    });
});