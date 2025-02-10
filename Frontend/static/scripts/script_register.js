document.querySelector("form").addEventListener("submit", async function(event) {
    event.preventDefault();  // Evita que la página se recargue

    let formData = new FormData(this);

    let response = await fetch("/register/", {
        method: "POST",
        body: formData
    });

    let data = await response.json();

    if (!response.ok) {
        // Si hay un error, muestra la ventana emergente con el mensaje
        Swal.fire({
            title: "¡Error!",
            text: data.error,  // El mensaje de error se pasa desde el backend
            icon: "error",
            background: "linear-gradient(120deg, #ec7879, #fff)",
            color: "#3d0c08",
            width: "400px", // Tamaño más pequeño de la ventana
            height: "200px", // Corregir 'heigth' a 'height'
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
        // Si el registro es exitoso, redirige a la página de login
        window.location.href = "/login/";  // Redirige a la página de login
    }
});
