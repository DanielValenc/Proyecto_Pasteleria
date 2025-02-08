function handleOtherInput(input) {
    const parent = input.closest('.section');
    const radioButtons = parent.querySelectorAll(`input[type="radio"][name="${input.name.split('-')[0]}"]`);

    if (input.value.trim() !== '') {
        radioButtons.forEach(radio => {
            radio.disabled = true;
        });
    } else {
        radioButtons.forEach(radio => {
            radio.disabled = false;
        });
    }
}

function submitForm() {
    const formElements = document.forms["cakeForm"].elements;
    let formData = {};

    for (let element of formElements) {
        const name = element.name.split('-')[0];

        // Si es un input de texto y tiene un valor
        if (element.type === 'text' && element.value.trim() !== '') {
            if (!formData[name]) {
                formData[name] = []; // Crea un array si no existe
            } else if (!Array.isArray(formData[name])) {
                formData[name] = [formData[name]]; // Convierte a array si es un string
            }
            formData[name].push(element.value.trim()); // Agrega el valor del input al array
        }
        // Si es un checkbox y está seleccionado
        else if (element.type === 'checkbox' && element.checked) {
            if (!formData[name]) {
                formData[name] = []; // Crea un array si no existe
            } else if (!Array.isArray(formData[name])) {
                formData[name] = [formData[name]]; // Convierte a array si es un string
            }
            formData[name].push(element.value.trim()); // Agrega el valor del checkbox al array
        }
        // Si es un radio button y está seleccionado
        else if (element.type === 'radio' && element.checked) {
            formData[name] = element.value.trim(); // Asigna directamente el valor del radio
        }
    }

    // Convertir los arrays en cadenas legibles (opcional)
    for (let key in formData) {
        if (Array.isArray(formData[key])) {
            formData[key] = formData[key].join(", "); // Convierte arrays en strings
        }
    }

    let jsonData = JSON.stringify(formData); // Convertir a JSON
    

    return jsonData; // Devolver el JSON en formato de string
}


// Llamar a la función submitForm para enviar el formulario y generar las imágenes
async function handleSubmitForm() {
    const jsonData = submitForm(); // Obtener los datos del formulario como JSON
    console.log("Datos JSON antes de enviar:", jsonData);

    // Enviar los datos al backend para generar las imágenes
    try {
        const response = await fetch('/generate/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: jsonData
        });
    
        if (!response.ok) {
            throw new Error('Error en la generación de imágenes');
        }
    
        const data = await response.json();
        
        const imageUrls = data.image_urls;
        
        showImagesPopup(imageUrls);
    } catch (error) {
        console.error('Error:', error);
        alert('Hubo un problema al generar las imágenes. Intenta de nuevo.');
    }
}

// Mostrar las imágenes en una ventana emergente
function showImagesPopup(imageUrls) {
    const popup = document.getElementById("popup");
    const imageOptions = document.getElementById("imageOptions");

    // Limpiar el contenedor de imágenes
    imageOptions.innerHTML = '';

    // Crear imágenes a partir de las URLs
    imageUrls.forEach((url, index) => {
        if(url){
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