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

  var rowCount;
  var hedCount;
  var sortButton;
  var newSort;
  var t;  
    
  for (i=0; i<5; i++) {
    t = tables[i];
    if ($(`#table-${t}`)) {
      hedCount = $(`#table-${t} th`).length;
      rowCount = $(`#table-${t} tr`).length;
      newSort = 1;
      for (j=2; j<(hedCount+2); j++) {
        for (k=0; k<rowCount; k++) {
          $(`#${t}-${j}-datarow-${k}`).hide();
        }
        sortButton = document.getElementById(`${t}-sortasc-${j-2}`);
        console.log(sortButton);
        sortButton.addEventListener('click', function() {
          $(`#${t}-${newSort}-datarow-${k}`).hide();
          newSort = j;
          for (k=1; k<rowCount; k++) {
            $(`#${t}-${newSort}-datarow-${k}`).show();
          }
        });
      }
      for (j=(2+hedCount); j<(hedCount*2+2); j++) {
        for (k=0; k<rowCount; k++) {
          $(`#${t}-${j}-datarow-${k}`).hide();
        }
        sortButton = document.getElementById(`${t}-sortdesc-${j-2-hedCount}`);
        console.log(sortButton)
        sortButton.addEventListener('click', function() {
          $(`#${t}-${newSort}-datarow-${k}`).hide();
          newSort = j;
          for (k=1; k<rowCount; k++) {
            $(`#${t}-${newSort}-datarow-${k}`).show();
          }
        });
      }
    }
  }
    
});
