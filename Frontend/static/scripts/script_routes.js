


    document.addEventListener("DOMContentLoaded", function () {
       
    
        const btnGenerate = document.getElementById("btnGenerate");
    
        if (btnGenerate) {
            btnGenerate.addEventListener("click", function () {
                console.log("Contact button clicked");
                window.location.href = "/generate/";
            });
        }
    });
    