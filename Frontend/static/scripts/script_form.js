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
            img.onclick = () => selectImage(url);  // Seleccionar la imagen cuando se haga clic

            // Agregar la imagen al contenedor
            imageOptions.appendChild(img);
        }
    });

    // Mostrar el popup
    popup.style.display = "block";
}

// Función para seleccionar una imagen
let selectedImage = null;
function selectImage(url) {
    selectedImage = url;
    // Mostrar el botón de WhatsApp solo después de seleccionar una imagen
    document.getElementById("whatsappBtn").style.display = "block";
}

// Cerrar el popup
function closePopup() {
    document.getElementById("popup").style.display = "none";
}

// Redirigir al usuario a WhatsApp con la imagen seleccionada
function redirectToWhatsApp() {
    if (selectedImage) {
        const message = `Mira este diseño de pastel: ${selectedImage}`;
        const whatsappUrl = `https://wa.me/?text=${encodeURIComponent(message)}`;
        window.open(whatsappUrl, '_blank');
    }
}