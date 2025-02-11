// static/scripts/panel_pastelero.js

function cambiarEstado(pedidoId, nuevoEstado) {
    fetch(`/pedido/${pedidoId}/estado`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ estado: nuevoEstado }),
    })
    .then(response => response.json())
    .then(data => {
        alert(`El pedido ${pedidoId} ha sido actualizado a ${nuevoEstado}`);
        location.reload();  // Recargar para ver los cambios en la interfaz
    })
    .catch(error => console.error('Error:', error));
}
