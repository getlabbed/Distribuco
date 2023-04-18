// https://socket.io/docs/v4/
var socket = io.connect('http://0.0.0.0:5000'); // Remplacer l'adresse IP par l'adresse du RPI

socket.on('navigate', function(url) {
  // Rediriger seulement si le client est sur la page principale
  if (window.location.pathname === '/' || window.location.pathname === '/drinkcomplete') {  
    window.location.href = url;
  }
});

// Define variables to keep track of the selected box
var selectedRow = 0;
var selectedColumn = 0;
var rows = document.querySelectorAll('.row');

// Function to highlight the selected box
function highlightSelectedBox() {
  rows.forEach(function(row, rowIndex) {
    var boxes = row.querySelectorAll('.drink-tile-item');
    boxes.forEach(function(box, colIndex) {
      if (rowIndex === selectedRow && colIndex === selectedColumn) {
        box.classList.add('selected');
      } else {
        box.classList.remove('selected');
      }
    });
  });
}

// Listen for the 'keypad' event from the server
socket.on('keypad', function(data) {

  console.log('keypad event received: ' + data)
  
  if (data === '1' || data === '2' || data === '3') {
    selectedColumn = parseInt(data) - 1;
  } else if (data === 'UP') {
    selectedRow = Math.max(0, selectedRow - 1);
  } else if (data === 'DWN') {
    selectedRow = Math.min(rows.length - 1, selectedRow + 1);
  } else if (data === 'NTR') {
    var selectedForm = rows[selectedRow].querySelectorAll('.drink-tile-item')[selectedColumn].parentElement;
    selectedForm.submit();
  }
  
  highlightSelectedBox();
});

// Highlight the first box when the page loads
highlightSelectedBox();