function ajout() {
  const sliders = document.querySelectorAll('.slider');
  const cercles = document.querySelectorAll('.pourcentage');
  const cerclesForm = document.querySelectorAll('.pourcentageForm')
  const inputmL = document.querySelectorAll('.displayQty');
  const displayTotal = document.querySelectorAll('.displayTotal')
  const total = document.querySelector('.slider-total')
  const maxVolume = 355
  let totalVolume = 355;
  function updatePercentages() {
    let total = 0;
  
    sliders.forEach(slider => {
      total += parseInt(slider.value);
    });
  
    sliders.forEach((slider, index) => {
      const percentage = 100 * (parseInt(slider.value) / total);     // Calcul du pourcentage
      const bar = slider.nextElementSibling.nextElementSibling;      // Get la barre qui est le prochain élément
      bar.style.width = `${percentage}%`;                            // Appliquer le pourcentage aux barres
  
      // Update du pourcentage dans le cercle
      cercles[index].innerHTML = percentage.toFixed(1) + "%";        // Arrondir à 1 chiffre après la virgule, affecte aussi les entrées
      cerclesForm[index].value = percentage.toFixed(1);
  
      // Update des input de quantitées de liquides
      const volume = (percentage * totalVolume) / 100;               // Calcul du volume
      inputmL[index * 2].value = volume.toFixed(2);                  // 2 input à chaque ligne           (ml)
      inputmL[index * 2 + 1].value = (volume * 0.033814).toFixed(2); // Décalé de 1 pour l'input de plus (oz)
    });
  }
  sliders.forEach(slider => {
    slider.addEventListener('input', updatePercentages);
  });
  
  // Slider total
  total.addEventListener("input", function() {
    totalVolume = total.value * maxVolume / 100;
    const totalBar = total.nextElementSibling.nextElementSibling;
    const totalSliderWidth = total.offsetWidth;
    const knobPosition = (total.value / 100 * (totalSliderWidth - 20)) + 20; // le knob à un diamètre de 20 px

    // Position en px converti en %, ce qui fait en sorte que lorsqu'on change l'écran de résolution, la barre garde le pourcentage donné
    // Cela ne règle pas le problème parfaitement, puisque le pourcentage est différent selon la largeur de l'affichage
    const totalPercent = (knobPosition / totalSliderWidth) * 100;

    totalBar.style.width = `${totalPercent}%`;

    displayTotal.forEach((display, index) => {
      displayTotal[index * 2].value = totalVolume.toFixed(2);                 // (ml)
      displayTotal[index * 2 + 1].value = (totalVolume * 0.033814).toFixed(2) // (oz)
    });
    console.log(total.value, knobPosition, totalPercent);
    updatePercentages();
  });
}

document.addEventListener('DOMContentLoaded', ajout);     // Exécuter le code quand la page est chargée

// Événements Swup https://swup.js.org/events
document.addEventListener('swup:contentReplaced', ajout); // Exécuter le code quand la page est chargée par Swup

