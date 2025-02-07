document.addEventListener('DOMContentLoaded', function() {
    // Asignar eventos a los botones del header
    document.getElementById('homeBtn').addEventListener('click', function() {
        console.log("Home button clicked");
        window.location.href = '/home/';
    });

    document.getElementById('formBtn').addEventListener('click', function() {
        console.log("Form button clicked");
        window.location.href = '/generate/';
    });

    document.getElementById('productsBtn').addEventListener('click', function() {
        console.log("Products button clicked");
        window.location.href = '/products/';
    });

    

    document.getElementById('btnGenerate').addEventListener('click', function() {
        console.log("Contact button clicked");
        window.location.href = '/generate/';
    });

    

    // Manejar el envío del formulario
    document.querySelector("form").addEventListener("submit", async (event) => {
        event.preventDefault(); // Evita que el formulario se envíe automáticamente

        const formData = new FormData(event.target);

        // Enviar datos al backend
        const response = await fetch("/generate/", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({
                forma: formData.get("forma"),
                porciones: formData.get("porciones"),
                cubierta: formData.get("cubierta"),
                distribucion: formData.get("distribucion"),
                decoracion: formData.getAll("decoracion"),
                mensajePastel: formData.get("mensajePastel"),
                personalizacion: formData.get("personalizacion"),
            }),
        });

        const result = await response.json();
        console.log("Respuesta del servidor:", result);

        // Mostrar las imágenes generadas
        if (result.generated_images) {
            const shareMessage = document.getElementById("shareMessage");
            const generatedImages = document.getElementById("generatedImages");
            const shareBtn = document.getElementById("shareBtn");

            shareMessage.style.display = "block";
            generatedImages.innerHTML = result.generated_images
                .map(
                    (img, index) => `
                    <div class="image-item" style="cursor: pointer;">
                        <img src="${img.url}" alt="Imagen ${index}" style="width: 100px; height: 100px;" onclick="selectImage('${img.url}')">
                    </div>
                `
                )
                .join("");

            shareBtn.style.display = "inline-block";
        }
    });
});

// Función para seleccionar la imagen
function selectImage(imageUrl) {
    selectedImage = imageUrl;
    document.getElementById("shareBtn").style.display = "inline-block";
}

// Función para compartir la imagen seleccionada en WhatsApp
document.getElementById("shareBtn").addEventListener("click", () => {
    if (selectedImage) {
        const whatsappUrl = `https://wa.me/?text=¡Mira este pastel! ${selectedImage}`;
        window.open(whatsappUrl, "_blank");

        // Subir la imagen seleccionada a Backblaze
        uploadImageToBackblaze(selectedImage);
    }
});

// Función para subir la imagen seleccionada a Backblaze (implementación simple)
async function uploadImageToBackblaze(imageUrl) {
    try {
        const response = await fetch("/upload-to-backblaze/", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({ imageUrl }),
        });

        const result = await response.json();
        if (result.success) {
            alert("Imagen subida a Backblaze exitosamente");
        } else {
            alert("Hubo un problema al subir la imagen");
        }
    } catch (error) {
        console.error("Error al subir la imagen a Backblaze:", error);
        alert("Hubo un problema al subir la imagen a Backblaze");
    }
}