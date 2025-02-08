document.addEventListener("DOMContentLoaded", function() {
    const form = document.getElementById("registration-form");
    if (form) {
        form.addEventListener("submit", function(event) {
            event.preventDefault(); // Evita que el formulario se envíe de forma tradicional
            
            // Captura los valores de los campos
            const username = document.getElementById('username').value;
            const fullName = document.getElementById('full_name').value;
            const phoneNumber = document.getElementById('numTel').value;
            const email = document.getElementById('email').value;
            const password = document.getElementById('password').value;
        
            // Crea un objeto con los datos del formulario
            const userData = {
                username: username,
                full_name: fullName,
                phone_number: phoneNumber,
                email: email,
                password: password
            };
        
            // Realiza la solicitud POST con fetch
            fetch('http://localhost:8000/register/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(userData)  // Enviar los datos como JSON
            })
            .then(response => response.json())
            .then(data => {
                console.log(data);  // Maneja la respuesta del servidor
                // Aquí puedes manejar la respuesta, como mostrar un mensaje de éxito
            })
            .catch(error => {
                console.error('Error:', error);
                // Aquí puedes manejar el error, como mostrar un mensaje de error
            });
        });
    }
});
