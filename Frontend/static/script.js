


// Asignar eventos a los botones del header
document.getElementById('homeBtn').addEventListener('click', function() {
    window.location.href = "/";
});

document.getElementById('formBtn').addEventListener('click', function() {
    window.location.href = "/form";
});

document.getElementById('productsBtn').addEventListener('click', function(e) {
    window.location.href = "/products";
});

document.getElementById('contactBtn').addEventListener('click', function(e) {
    window.location.href = "/contact";
});