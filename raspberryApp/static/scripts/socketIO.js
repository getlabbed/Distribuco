// https://socket.io/docs/v4/
var socket = io.connect('http://192.168.202.31:5000'); // Changer l'adresse à 0.0.0.0 pour la machine finale

socket.on('navigate', function(url) {
  // Rediriger seulement si le client est sur la page principale
  if (window.location.pathname === '/') {  
    window.location.href = url;
  }
});