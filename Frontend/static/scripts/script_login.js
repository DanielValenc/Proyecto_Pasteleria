document.getElementById("btnLogin").addEventListener("submit", async function (event) {
    event.preventDefault(); // Evita que el formulario recargue la página
    
    const formData = new FormData(this);
    const username = formData.get("username");
    const password = formData.get("password");

    try {
        const response = await fetch("http://127.0.0.1:8000/login/", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                username: username,
                password: password
            })
        });

        const data = await response.json();

        if (response.ok) {
            alert("✅ ¡Inicio de sesión exitoso! Redirigiendo...");
            localStorage.setItem("access_token", data.access_token); // Guardar token en localStorage
            window.location.href = "/dashboard"; // Redirigir al usuario
        } else {
            alert("❌ Error: " + data.detail); // Mostrar error
        }
    } catch (error) {
        console.error("Error:", error);
        alert("⚠️ Ocurrió un problema. Inténtalo de nuevo.");
    }
});

