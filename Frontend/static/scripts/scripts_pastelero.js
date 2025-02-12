document.addEventListener("DOMContentLoaded", function () {
    fetch('/pastelero/pedidos/')
        .then(response => {
            if (!response.ok) {
                throw new Error(`Error HTTP: ${response.status} - ${response.statusText}`);
            }
            return response.json();
        })
        .then(data => {
            const pedidosList = document.getElementById('pedidosList');

            console.log("Datos de los pedidos recibidos:", data); // Verificar datos en consola

            pedidosList.innerHTML = ""; // Limpiar lista antes de agregar pedidos

            if (data.length > 0) {
                data.forEach(pedido => {
                    // Crear contenedor del pedido
                    const li = document.createElement('li');
                    li.classList.add("pedido-container");

                    // Estructura en dos columnas
                    li.innerHTML = `
                        <div class="pedido-info">
                            <p><strong>Temática:</strong> ${pedido.tematica}</p>
                            <p><strong>Sabor:</strong> ${pedido.cake_type}</p>
                            <p><strong>Forma:</strong> ${pedido.cake_shape}</p>
                            <p><strong>Tamaño:</strong> ${pedido.cake_size}</p>
                            <p><strong>Decoración:</strong> ${pedido.decoration}</p>
                            ${pedido.menssage ? `<p><strong>Mensaje:</strong> "${pedido.menssage}"</p>` : ""}
                           
                        </div>
                        <div class="pedido-imagen">
                            ${pedido.image_url ? `<img src="${pedido.image_url}" alt="Imagen del pastel">` : "<p>Imagen no disponible</p>"}
                        </div>
                    `;

                    

                    pedidosList.appendChild(li);
                });
            } else {
                pedidosList.innerHTML = "<p>No hay pedidos asignados</p>";
            }
        })
        .catch(error => {
            console.error('Error al cargar los pedidos:', error);
            document.getElementById('pedidosList').innerHTML = `<p class="error-text">Hubo un problema al cargar los pedidos: ${error.message}</p>`;
        });
});
