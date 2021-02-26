$(document).ready(function() {
    
  var scrollTop;
  var scrollLeft;
  var scrollPoint;
  var trueDivHeight;
  var divHeight;
  var scrollBottom;
    
  var container = document.getElementById('container');
  $(window).width() > 500 ? scrollPoint = 824 : scrollPoint = 643;
    
  $('#container').scroll(function() {
    scrollTop = $('#container').scrollTop();
    scrollLeft = $('#container').scrollLeft();
    trueDivHeight = $('#container')[0].scrollHeight;
    divHeight = $('#container').height();
    scrollBottom = trueDivHeight - divHeight;
      
    scrollTop >= scrollPoint || scrollBottom == scrollTop ? 
    container.style.overflowX = 'scroll' : container.style.overflowX = 'hidden';
    scrollTop < scrollPoint && scrollLeft !== 0 ? 
    $('#container').scrollTop(scrollPoint) : '';
  });
 
  var tables = ['balance', 'income', 'operations', 'equity', 'cash'];
  var wordArr = ['Total', 'Gross', 'Loss Before', 'Loss from', 'Net loss', 'Net cash', 'Net increase', 'Balance'];
  var dblArr = ['Total assets'];
  var idxCount = 0;
  var contin = false;
  var tAcct;
  var tData;
  var wordAcct;
  var wordOne;
  var wordTwo;
  var wordThree;

  for (i=0; i<tables.length; i++) {
    while (contin == false) {
      tAcct = false;
      tAcct = document.getElementById(`${tables[i]}-acct-${idxCount}`);
      if (tAcct) {
        wordAcct = tAcct.innerHTML.trim().split(' ');
        wordOne = wordAcct[0].trim(',');
        wordTwo = `${wordAcct[0]} ${wordAcct[1]}`;
        wordThree = `${wordAcct[0]} ${wordAcct[1]} ${wordAcct[2]}`;
        if (wordArr.indexOf(wordOne) > -1 || wordArr.indexOf(wordTwo) > -1) {
          tData = document.querySelectorAll(`.${tables[i]}-data-${idxCount}`);
          tData.forEach(data => {
            data.style.borderTop = 'solid 2px #000';
            data.classList.add('acct-line');
            data.innerHTML = `$ ${data.innerHTML.trim()}`;
          });
          tData = undefined;
        }
        if (dblArr.indexOf(wordThree) > -1 || dblArr.indexOf(wordTwo) > -1) {
          tData = document.querySelectorAll(`.${tables[i]}-data-${idxCount}`);
          tData.forEach(data => {
            data.style.borderBottom = 'thick double #000';
            data.classList.add('acct-thick');
            if (data.innerHTML.trim()[0] !== '$') {
              data.innerHTML = `$ ${data.innerHTML.trim()}`;
            }
          });
          tData = undefined;
        } 
        idxCount++;
        tAcct = false;
      } else {
        idxCount = 0;
        contin = true;
      }
    }
    contin = false;
  }
    
});
