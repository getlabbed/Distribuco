// Code fait par chatGPT

$('.color').colorPicker({
    // Autres options
    renderCallback: function($elm) {
        var hexValue = this.color.colors.HEX; // Récupérer la valeur hexadécimale
        // Afficher la valeur hexadécimale
        $elm.val('#' + hexValue);
    },
});