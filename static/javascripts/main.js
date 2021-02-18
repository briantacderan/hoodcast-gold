$(document).ready(function() {  
    
  var idx = 0;
  var body = document.querySelector('body');
  var container = document.getElementById('container');

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

  var selector = document.getElementById('balance-selector');
  var dfName = selector.value;
  console.log(dfName);

  selector.addEventListener('click', function() {
    if (selector.value != dfName) {
      console.log(dfName);
      $(`#to-${dfName}`).hide();
      handleChange();
    }
  });
    
  selector.addEventListener('change', function() {
    if (selector.value != dfName) {
      console.log(dfName);
      $(`#to-${dfName}`).hide();
        
      dfName = selector.value;
      $(`#to-${dfName}`).show();
    }
  });
});
