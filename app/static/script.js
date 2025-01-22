// Almacenará los valores seleccionados
const selectedValues = {};

// Manejo de selección para radio buttons
document.querySelectorAll("input[type='radio']").forEach((radio) => {
    radio.addEventListener("change", (event) => {
        const groupName = event.target.name; // Obtener el nombre del grupo (forma o estilo)
        const value = event.target.value; // Obtener el valor seleccionado
        selectedValues[groupName] = value; // Guardar el valor en selectedValues
    });
});

// Manejo del botón "Generar Pastel"
document.getElementById("submitBtn").addEventListener("click", async () => {
    // Capturar valores de los campos normales
    const porciones = document.getElementById("porciones").value.trim();
    const sabor = document.getElementById("sabor").value.trim();
    const topping = document.getElementById("topping").value.trim();
    const tematica = document.getElementById("tematica").value.trim();
    const color = document.getElementById("color").value.trim();
    const decoracion = document.getElementById("decoracion").value.trim();
    const mensaje = document.getElementById("mensage").value.trim();

    // Validar que todos los valores requeridos estén seleccionados
    if (
        !porciones ||
        !sabor ||
        !topping ||
        !tematica ||
        !color ||
        !decoracion ||
        !mensaje ||
        !selectedValues["forma"] || // Asegurarse de que "forma" esté seleccionado
        !selectedValues["estilo"]  // Asegurarse de que "estilo" esté seleccionado
    ) {
        alert("Por favor, completa todos los campos obligatorios.");
        return;
    }

    // Enviar datos al backend
    try {
        const response = await fetch("/generate/", {
            method: "POST",
            headers: {
                "Content-Type": "application/x-www-form-urlencoded",
            },
            body: new URLSearchParams({
                porciones,
                sabor,
                topping,
                tematica,
                color,
                decoracion,
                mensaje,
                forma: selectedValues["forma"], // Valor del radio button seleccionado para forma
                estilo: selectedValues["estilo"], // Valor del radio button seleccionado para estilo
            }),
        });

        if (response.ok) {
            const html = await response.text();
            document.body.innerHTML = html; // Mostrar respuesta del backend
        } else {
            alert("Error al generar el pastel. Inténtalo nuevamente.");
        }
    } catch (error) {
        console.error("Error:", error);
        alert("Ocurrió un error. Revisa la consola para más detalles.");
    }
});
