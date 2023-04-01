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

// Viens metttre en sélection le premier chiffre pour le TOPT
window.onload = function() {
    document.getElementById("totp1").focus();
  };

// Fonction qui préviens l'utilisateur de mettre des caratères autre que des chiffres
function validateNumericInput(input) {
input.value = input.value.replace(/[^\d]/g, ''); // utilisation d'un regex
}