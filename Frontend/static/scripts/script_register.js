document.querySelector("form").addEventListener("submit", async function(event) {
    event.preventDefault();  // Evita que la página se recargue

    let formData = new FormData(this);

    // Asegúrate de que el valor del tipo de usuario esté incluido
    let userType = document.querySelector("#userType").value;
    formData.append("userType", userType);

    let response = await fetch("/register/", {
        method: "POST",
        body: formData
    });

    let data = await response.json();
    console.log(data); // Para ver el contenido de la respuesta

    if (!response.ok) {
        // Si hay un error, muestra la ventana emergente con el mensaje
        Swal.fire({
            title: "¡Error!",
            text: data.error,  // El mensaje de error se pasa desde el backend
            icon: "error",
            background: "linear-gradient(120deg, #ec7879, #fff)",
            color: "#3d0c08",
            width: "400px",
            height: "200px",
            padding: "20px",
            confirmButtonColor: "#3d0c08",
            confirmButtonText: "Ok",
            customClass: {
                title: 'swal-title', 
                content: 'swal-content', 
                confirmButton: 'swal-button' 
            }
        });
    } else {
        // Si el registro es exitoso, redirige a la página de login
        window.location.href = "/login/";  // Redirige a la página de login
    }
});
