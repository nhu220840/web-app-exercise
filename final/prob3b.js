document.addEventListener("DOMContentLoaded", () => {
    const form = document.querySelector("form"); // lấy form đầu tiên
    form.addEventListener("submit", function(event) {
        // Gọi hàm validScore đã có sẵn
        if (!validScore(event)) {
            event.preventDefault(); // ngăn submit nếu invalid
        }
    });
});