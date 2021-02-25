$(document).ready(function() {
  
  var isScroll = document.getElementById('container');
  var scrollPoint;
    
  if ($(window).width() > 500) {  
    scrollPoint = 819;
    $('#container').scroll(function() {
      $('#container').scrollTop() >= scrollPoint ? 
      isScroll.style.overflowX = 'scroll' : isScroll.style.overflowX = 'hidden';
      $('#container').scrollTop() < scrollPoint && $('#container').scrollLeft() !== 0 ?
      $('#container').scrollTop(scrollPoint) : '';
    });
  } else {
    scrollPoint = 638;
    $('#container').scroll(function() {
      $('#container').scrollTop() >= scrollPoint ? 
      isScroll.style.overflowX = 'scroll' : isScroll.style.overflowX = 'hidden';
      $('#container').scrollTop() < scrollPoint && $('#container').scrollLeft() !== 0 ?
      $('#container').scrollTop(scrollPoint) : '';
    });
  }
 
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
