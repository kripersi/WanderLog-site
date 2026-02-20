document.addEventListener("DOMContentLoaded", function () {
    const input = document.getElementById("id_avatar");
    const avatarImage = document.querySelector(".avatar img");

    if (input) {
        input.addEventListener("change", function (event) {
            const file = event.target.files[0];
            if (file) {
                const reader = new FileReader();

                reader.onload = function (e) {
                    avatarImage.src = e.target.result;
                };

                reader.readAsDataURL(file);
            }
        });
    }
});