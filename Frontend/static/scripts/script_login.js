document.querySelector("form").addEventListener("submit", async function(event) {
    event.preventDefault();  // Evita que la página se recargue

    let formData = new FormData(this);

    // Enviar datos al backend
    let response = await fetch("/login/", {
        method: "POST",
        body: formData
    });

    // Convertir la respuesta a JSON
    let data = await response.json();

    // Verifica si la respuesta es OK
    if (!response.ok) {
        Swal.fire({
            title: "¡Error!",
            text: data.detail || "Usuario o contraseña incorrectos.",
            icon: "error",
            background: "linear-gradient(120deg, #ec7879, #fff)",
            color: "#3d0c08",
            width: "400px", // Tamaño más pequeño de la ventana
            heigth:" 200px",
            padding: "20px", // Añadir padding para que el contenido no quede pegado
            confirmButtonColor: "#3d0c08",
            confirmButtonText: "Ok",
            customClass: {
                title: 'swal-title',  // Cambiar estilo solo del título
                content: 'swal-content',  // Cambiar estilo solo del contenido
                confirmButton: 'swal-button'  // Cambiar estilo solo del botón
            }
        });
    } else {
        // Si el login es exitoso, redirige directamente a la página home
        window.location.href = "/home/";  // Redirige a la página principal
    }
});
