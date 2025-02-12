
function generateCake() {
    const tematica = document.getElementById('tematica').value;
    const cakeType = document.getElementById('cake-type').value;
    const cakeShape = document.getElementById('cake-shape').value;
    const cakeSize = document.getElementById('cake-size').value;
    const decoration = document.getElementById('decoration').value;
    const message = document.getElementById('message').value;
    

    const data = {
        tematica: tematica,
        cake_type: cakeType,
        cake_shape:cakeShape,
        cake_size: cakeSize,
        decoration: decoration,
        message:message
        
    };
   
    console.log("Datos a enviar:", data);
    fetch('/generate/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
    })
        .then(response => {
            if (!response.ok) {
                return response.json().then(err => { throw new Error(err.detail || 'Error en la solicitud'); });
            }
            return response.json();
        })
          
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


//**********FUNCION PARA ALMACENAR ORDEN*********** */

// Agregar el evento al botón de enviar
document.getElementById('submitOrderButton').addEventListener('click', handleSubmitForm);

function handleSubmitForm(event) {
    event.preventDefault();

    const selectedImage = document.getElementById('imagenSeleccionada').value;
    if (!selectedImage) {
        alert("Por favor, selecciona una imagen.");
        return;
    }

    const tematica = document.getElementById('tematica').value;
    const cakeType = document.getElementById('cake-type').value;
    const cakeShape = document.getElementById('cake-shape').value;
    const cakeSize = document.getElementById('cake-size').value;
    const decoration = document.getElementById('decoration').value;
    const message = document.getElementById('message').value;
    
    // Verificar que los campos obligatorios no estén vacíos
    if (!tematica || !cakeType || !cakeShape || !cakeSize || !decoration) {
        alert("Por favor, completa todos los campos obligatorios.");
        return;
    }

    // Obtener un pastelero aleatorio antes de enviar la orden
    fetch('/pastelero-random/')
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                alert("No hay pasteleros disponibles.");
                return;
            }

            const pasteleroId = data.pastelero_id;

            const orderData = {
                tematica: tematica,
                cake_type: cakeType,
                cake_shape: cakeShape,
                cake_size: cakeSize,
                decoration: decoration,
                message: message,
                image_url: selectedImage,
                pastelero_id: pasteleroId,
            };

            console.log(orderData);  // Verifica los datos a enviar

            // Enviar la orden con el pastelero asignado
            return fetch('/guardarOrden/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(orderData)
            });
        })
        .then(response => response.json())
        .then(data => {
            console.log('Orden guardada con éxito:', data);
            alert("¡Tu pedido ha sido realizado exitosamente! Pronto se comunicarán contigo");
        })
        .catch((error) => {
            console.error('Error al guardar la orden:', error);
            alert('Hubo un error al guardar la orden. Intenta nuevamente más tarde.');
        });
}



// Función para seleccionar una imagen
let selectedImage = null;

function selectImage(url, imgElement) {
    const imagenSeleccionada = document.getElementById('imagenSeleccionada');
    imagenSeleccionada.value = url;  // Establecer la URL de la imagen seleccionada en el campo oculto

    // Remover la clase "selected" de todas las imágenes antes de seleccionar otra
    document.querySelectorAll("#imageOptions img").forEach(img => {
        img.classList.remove("selected");
    });

    // Agregar la clase "selected" a la imagen actual
    imgElement.classList.add("selected");

    // Habilitar el botón de enviar solo después de seleccionar una imagen
    document.getElementById("submitOrderButton").disabled = false;
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
