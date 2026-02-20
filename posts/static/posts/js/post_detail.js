document.addEventListener("DOMContentLoaded", function () {

    let currentIndex = 0;
    const images = document.querySelectorAll(".gallery-image");
    const modal = document.getElementById("imageModal");
    const modalImg = document.getElementById("modalImage");

    function showImage(index) {
        images.forEach(img => img.style.display = "none");
        if (images[index]) {
            images[index].style.display = "block";
        }
    }

    function nextImage() {
        currentIndex = (currentIndex + 1) % images.length;
        showImage(currentIndex);
    }

    function prevImage() {
        currentIndex = (currentIndex - 1 + images.length) % images.length;
        showImage(currentIndex);
    }

    images.forEach(img => {
        img.addEventListener("click", function () {
            modal.style.display = "flex";
            modalImg.src = this.src;
        });
    });

    function closeModal() {
        modal.style.display = "none";
    }

    modal.addEventListener("click", function (e) {
        if (e.target === modal) {
            closeModal();
        }
    });

    document.addEventListener("keydown", function (e) {
        if (e.key === "Escape") {
            closeModal();
        }
    });

    if (images.length > 0) {
        showImage(currentIndex);
    }

    // Делаем функции доступными для кнопок
    window.nextImage = nextImage;
    window.prevImage = prevImage;
    window.closeModal = closeModal;

});
