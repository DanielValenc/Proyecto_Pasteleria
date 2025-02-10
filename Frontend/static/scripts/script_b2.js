document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById("upload-form");
    if (form) {
        form.onsubmit = async (event) => {
            event.preventDefault();
            const formData = new FormData(event.target);
            const response = await fetch("/upload_image_and_redirect/", {
                method: "POST",
                body: formData,
            });

            if (response.ok) {
                window.location.href = await response.text();
            } else {
                alert("Error al subir la imagen.");
            }
        };
    }
});
