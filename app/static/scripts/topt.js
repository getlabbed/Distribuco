// Fonction pour le visuel de l'input TOPT: https://codepen.io/Aixoxa/pen/wvGYjbe
function clickEvent(first,last){
    if(first.value.length){
        // La condition if else permet d'éviter un problème, puisqu'à la dernière case, l'id 'soumettre' n'existe pas
        if(last == 'soumettre'){
            first.form.submit();
        }
        else{
            document.getElementById(last).focus();
        }
    }
}
// Fonction qui regarde si l'élément actuel à un chiffre ou non
function checkEmpty(current, previous, event){
    if(current.value.length == 0 && event.keyCode == 8){ // 8 is the code for the backspace key
        document.getElementById(previous).focus();
    }
}

// Fonction qui préviens l'utilisateur de mettre des caratères autre que des chiffres
function validateNumericInput(input) {
input.value = input.value.replace(/[^\d]/g, ''); // utilisation d'un regex
}

// Exécuter le code quand la page est chargée
document.addEventListener('DOMContentLoaded', function() {
    // Viens metttre en sélection le premier chiffre pour le TOPT
    window.onload = function() {
        document.getElementById("totp1").focus();
    };
});

// Événements Swup https://swup.js.org/events
// Exécuter le code quand la page est chargée par Swup 
document.addEventListener('swup:contentReplaced', function() {
    document.getElementById("totp1").focus();
});