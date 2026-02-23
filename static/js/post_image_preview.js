(() => {
    const input = document.getElementById('id_images');
    const preview = document.getElementById('image-preview');

    if (!input || !preview) {
        return;
    }

    const renderEmpty = () => {
        preview.innerHTML = '<div class="image-preview-empty">No photos selected.</div>';
    };

    const renderFiles = (files) => {
        preview.innerHTML = '';

        if (!files || files.length === 0) {
            renderEmpty();
            return;
        }

        Array.from(files).forEach((file) => {
            const item = document.createElement('div');
            item.className = 'image-preview-item';

            const img = document.createElement('img');
            img.alt = file.name;

            const name = document.createElement('div');
            name.className = 'image-preview-name';
            name.textContent = file.name;

            item.appendChild(img);
            item.appendChild(name);
            preview.appendChild(item);

            const reader = new FileReader();
            reader.onload = (event) => {
                img.src = event.target?.result;
            };
            reader.readAsDataURL(file);
        });
    };

    renderEmpty();

    input.addEventListener('change', (event) => {
        const files = event.target?.files;
        renderFiles(files);
    });
})();
