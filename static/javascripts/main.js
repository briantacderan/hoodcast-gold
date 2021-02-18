$(document).ready(function() {  
    
  var idx = 0;
  var body = document.querySelector('body');
  var container = document.getElementById('container');
    
  var dfName = document.getElementById('balance-selector').value;
  var oldName;
  
  body.style.background = 'white';
  container.style.height = '75vh';
      
  var tables = ['balance', 'income', 'operations', 'equity', 'cash'];
  for (i=0; i<5; i++) {
    if ($(`#to-${tables[i]}`)) {
      if (i !== idx) {
        $(`#to-${tables[i]}`).hide();
      } else {
        var hedCount = $(`#table-${tables[i]} th`).length; 
      }
    }
  }
    
  document.querySelectorAll('.selectors').forEach(item => {
    item.addEventListener('change', function() {
      if (item.value != dfName) {
        $(`#to-${dfName}`).hide();
        oldName = dfName.slice();
        dfName = item.value;
        $(`#to-${dfName}`).show();
        document.getElementById(`${oldName}-selector`).value = oldName;
      }
    });
  });
    
  /*document.querySelectorAll('.table-start').forEach(page => {
    console.log(document.getElementById('')
  });  
    
  for (i=0; i<hedCount; i++) {
    $(`#table-${dfName} .sortasc-${i}`)
  }*/ 
      
});
