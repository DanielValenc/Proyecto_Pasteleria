


    document.addEventListener("DOMContentLoaded", function () {
        document.getElementById('productsBtn').addEventListener('click', function() {
            console.log("Products button clicked");
            window.location.href = '/products/';
        });
    
        const btnGenerate = document.getElementById("btnGenerate");
    
        if (btnGenerate) {
            btnGenerate.addEventListener("click", function () {
                console.log("Contact button clicked");
                window.location.href = "/generate/";
            });
        }
    });
    