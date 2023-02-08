// Conversion du volume des liquides
function convertirVolume(quantite, unite) {
    if (unite == 'ml') {
      return quantite / 29.5735;
    }
    else {
      return quantite * 29.5735;
    }
  }