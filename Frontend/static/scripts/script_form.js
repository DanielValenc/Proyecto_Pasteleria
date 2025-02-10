function handleSubmitForm() {
    const tematica = document.getElementById('tematica').value;
    const cakeType = document.getElementById('cake-type').value;
    const cakeSize = document.getElementById('cake-size').value;
    const decoration = document.getElementById('decoration').value;
    const message = document.getElementById('message').value;

    const data = {
        tematica: tematica,
        cake_type: cakeType,
        cake_size: cakeSize,
        decoration: decoration,
        message: message
    };

    fetch('/generate/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
    })
        .then(response => response.json())
        .then(data => {
            console.log('Success:', data);

            // Asegúrate de que la respuesta contenga las URLs de las imágenes
            if (data.generated_images && data.generated_images.length > 0) {
                const imageUrls = data.generated_images.map(image => image.url);
                console.log(imageUrls)
                showImagesPopup(imageUrls);  // Llama a la función para mostrar las imágenes en el popup
            } else {
                console.error('No se encontraron imágenes generadas.');
            }
        })
        .catch((error) => {
            console.error('Error:', error);
        });
}




// Función para seleccionar una imagen
let selectedImage = null;

function selectImage(url, imgElement) {
    selectedImage = url;

    // Remover la clase "selected" de todas las imágenes antes de seleccionar otra
    document.querySelectorAll("#imageOptions img").forEach(img => {
        img.classList.remove("selected");
    });

    // Agregar la clase "selected" a la imagen actual
    imgElement.classList.add("selected");

    // Mostrar el botón de WhatsApp solo después de seleccionar una imagen
    document.getElementById("whatsappBtn").style.display = "block";
}

// Modificar la función para mostrar imágenes y agregar eventos de selección
function showImagesPopup(imageUrls) {
    const popup = document.getElementById("popup");
    const imageOptions = document.getElementById("imageOptions");

    // Limpiar el contenedor de imágenes antes de agregar nuevas
    imageOptions.innerHTML = '';

    // Crear imágenes a partir de las URLs recibidas
    imageUrls.forEach((url, index) => {
        if (url) {
            const img = document.createElement("img");
            img.src = url;
            img.alt = `Imagen ${index + 1}`;
            img.style.width = "150px";
            img.style.margin = "10px";
            img.onclick = () => selectImage(url, img);  // Seleccionar la imagen al hacer clic

            // Agregar la imagen al contenedor
            imageOptions.appendChild(img);
        }
    });

    // Mostrar el popup
    popup.style.display = "block";
}
// Redirigir al usuario a WhatsApp con la imagen seleccionada
async function redirectToWhatsApp() {
    if (selectedImage) {
        try {
            // Obtener el correo del usuario (debe ser dinámico en el backend)
            const userEmail = "dayalex9@hotmail.com";

            // Enviar la URL de la imagen seleccionada al backend para subirla
            const response = await fetch("/upload_image_and_redirect/", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ imageUrl: selectedImage, userEmail: userEmail })
            });

            const data = await response.json();
            if (response.ok && data.uploadedImageUrl) {
                // Crear el mensaje con la URL de la imagen subida
                const message = `Mira este diseño de pastel: ${data.uploadedImageUrl}`;
                const whatsappUrl = `https://wa.me/?text=${encodeURIComponent(message)}`;

                // Redirigir a WhatsApp
                window.open(whatsappUrl, '_blank');
            } else {
                alert("Error al subir la imagen.");
            }
        } catch (error) {
            console.error("Error al subir la imagen:", error);
        }
    }
}
