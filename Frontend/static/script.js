
document.getElementById("submitBtn").addEventListener("click", async () => {
    const formData = new FormData(document.querySelector("form"));
    //const pasteleroId = document.getElementById("pastelero_id").value;

    console.log("Forma:", formData.get("forma"));
    console.log("Porciones:", formData.get("porciones"));
    console.log("Cubierta:", formData.get("cubierta"));
    console.log("Distribución:", formData.get("distribucion"));
    console.log("Decoración:", formData.getAll("decoracion"));
    console.log("Mensaje:", formData.get("mensajePastel"));
    console.log("Personalización:", formData.get("personalizacion"));

    // Enviar datos al backend
    const response = await fetch("/generate", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({
            pastelero_id: pasteleroId,
            forma: formData.get("forma"),
            porciones: formData.get("porciones"),
            cubierta: formData.get("cubierta"),
            distribucion: formData.get("distribucion"),
            decoracion: formData.getAll("decoracion"),
            mensajePastel: formData.get("mensajePastel"),
            personalizacion: formData.get("personalizacion"),
        }),
    });

    const resultK = await response.json();
    console.log("Respuesta del servidor:", result);



    const result = await response.json();
    const imagenesContainer = document.getElementById("imagenes-container");
    const shareMessage = document.getElementById("shareMessage"); // Contenedor para mostrar imágenes
    const generatedImages = document.getElementById("generatedImages"); // Donde se mostrarán las imágenes generadas
    const shareBtn = document.getElementById("shareBtn"); // Botón para compartir en WhatsApp
    let selectedImage = ''; // Variable para almacenar la imagen seleccionada

    // Mostrar las imágenes generadas
    if (result.generated_images) {
        // Mostrar el contenedor de imágenes generadas
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

        // Mostrar el botón para compartir
        shareBtn.style.display = "inline-block";
    }
});

// Función para seleccionar la imagen
function selectImage(imageUrl) {
    selectedImage = imageUrl;
    // Mostrar el botón de compartir
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
        const response = await fetch("/upload-to-backblaze", {
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

// Asignar eventos a los botones del header



document.addEventListener('DOMContentLoaded', function() {

    // Asignar eventos a los botones del header

    document.getElementById('IniciarSecionBtn').addEventListener('click', function() {
        window.location.href = "/";
     });


    document.getElementById('homeBtn').addEventListener('click', function() {
         window.location.href = "/home";
     });


    document.getElementById('formBtn').addEventListener('click', function() {
          window.location.href = '/generate';
    });

    document.getElementById('productsBtn').addEventListener('click', function() {
         window.location.href = "/products";
    });

    document.getElementById('contactBtn').addEventListener('click', function() {
         window.location.href = "/contact";
    });
});
