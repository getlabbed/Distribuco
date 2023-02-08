const sliders = document.querySelectorAll('.slider');
const cercles = document.querySelectorAll('.pourcentage');
const cerclesForm = document.querySelectorAll('.pourcentageForm')
const inputmL = document.querySelectorAll('input[type="number"]');
const total = document.querySelector('.slider-total')
const maxVolume = 355
let totalVolume = 355;

function updatePercentages() {
  let total = 0;

  sliders.forEach(slider => {
    total += parseInt(slider.value);
  });

  sliders.forEach((slider, index) => {
    const percentage = 100 * (parseInt(slider.value) / total);   // Calcul du pourcentage
    const bar = slider.nextElementSibling.nextElementSibling;    // Get la barre qui est le prochain élément
    bar.style.width = `${percentage}%`;                          // Appliquer le pourcentage aux barres

    // Update du pourcentage dans le cercle
    cercles[index].innerHTML = percentage.toFixed(1) + "%";      // Arrondir à 1 chiffre après la virgule, affecte aussi les entrées
    cerclesForm[index].value = percentage.toFixed(1);

    // Update des input de quantitées de liquides
    const volume = (percentage * totalVolume) / 100;             // Calcul du volume
    inputmL[index * 2].value = volume;                           // 2 input à chaque ligne           (ml)
    inputmL[index * 2 +1 ].value = volume * 0.033814;            // Décalé de 1 pour l'input de plus (oz)
  });
}

sliders.forEach(slider => {
  slider.addEventListener('input', updatePercentages);
});

// Événement qui s'occupe d'updater le volume en mililitres
inputmL.forEach((input, index) => {
input.addEventListener("input", function() {
if (this.value < 0) {
  this.value = 0;
}
if (this.value > totalVolume) {
  this.value = totalVolume;
}
const volume = this.value / totalVolume * 100;
sliders[index].value = volume;
updatePercentages();
});
});
total.addEventListener("input", function() {
  totalVolume = total.value * maxVolume / 100;
  const totalBar = total.nextElementSibling.nextElementSibling;
  const totalSliderWidth = total.offsetWidth;
  const knobPosition = (total.value / 100 * (totalSliderWidth - 20)) + 20;
  totalBar.style.width = `${knobPosition}px`;
  console.log(total.value, knobPosition);
  updatePercentages();
});