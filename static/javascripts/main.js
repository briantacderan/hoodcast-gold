$(document).ready(function() {  
    
  var idx = 0;
  var body = document.querySelector('body');
  var container = document.getElementById('container');
  var dfName = document.getElementById('balance-selector').value;

  body.style.background = 'white';
  container.style.height = '75vh';
      
  var tables = ['balance', 'income', 'operations', 'equity', 'cash'];  
  for (i=0; i<5; i++) {
    if ($(`#to-${tables[i]}`)) {
      if (i !== idx) {
        $(`#to-${tables[i]}`).hide();
      }
    }
  }
    
  document.querySelectorAll('.selectors').forEach(item => {
    item.addEventListener('change', function() {
      if (item.value != dfName) {
        $(`#to-${dfName}`).hide();
        dfName = item.value;
        $(`#to-${dfName}`).show();
      }
    });
  });
    
});
