// Code fait par chatGPT

function color_wrapper(){
    $('.color').colorPicker({
        // Autres options
        renderCallback: function($elm) {
            var hexValue = this.color.colors.HEX; // Récupérer la valeur hexadécimale
            // Afficher la valeur hexadécimale
            $elm.val('#' + hexValue);
        },
    });
}


document.addEventListener('DOMContentLoaded', color_wrapper);     // Exécuter le code quand la page est chargée

// Événements Swup https://swup.js.org/events
document.addEventListener('swup:contentReplaced', color_wrapper); // Exécuter le code quand la page est chargée par Swup 