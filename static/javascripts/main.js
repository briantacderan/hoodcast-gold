$(document).ready(function() {  
    
  var idx = 0;
  var body = document.querySelector('body');
  var container = document.getElementById('container');
  var tables = ['balance', 'income', 'operations', 'equity', 'cash'];
    
  var dfName = document.getElementById('balance-selector').value;
  var oldName;
  
  container.setAttribute('class', 'new');
  body.style.background = 'white';
      
  for (var i=0; i<5; i++) {
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
  var oldSort;
  var t;  
    
  for (i=0; i<5; i++) {
    t = tables[i];
    if ($(`#table-${t}`)) {
      hedCount = $(`#table-${t} th`).length;
      rowCount = $(`#table-${t} tr`).length;
      oldSort = 1;
      for (var j=2; j<(hedCount+2); j++) {
        for (var k=0; k<rowCount; k++) {
          $(`#${t}-${j}-datarow-${k}`).hide();
        }
        sortButton = document.getElementById(`${t}-sortasc-${j-2}`);
        sortButton.addEventListener('mousedown', function() {
          for (var k=1; k<rowCount; k++) {
            $(`#${t}-${oldSort}-datarow-${k}`).hide();
            $(`#${t}-${j}-datarow-${k}`).show();
          }
          oldSort = j;
        });
      }
      for (var j=(2+hedCount); j<(hedCount*2+2); j++) {
        for (var k=0; k<rowCount; k++) {
          $(`#${t}-${j}-datarow-${k}`).hide();
        }
        sortButton = document.getElementById(`${t}-sortdesc-${j-2-hedCount}`);
        sortButton.addEventListener('mousedown', function() {
          for (var k=1; k<rowCount; k++) {
            $(`#${t}-${oldSort}-datarow-${k}`).hide();
            $(`#${t}-${j}-datarow-${k}`).show();
          }
          oldSort = j;
        });
      }
    }
  }
    
});
