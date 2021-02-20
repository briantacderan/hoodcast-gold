$(document).ready(function() {  
    
  (function($) {
    $('#hoodcast-logo path').hide();  
    
    $.fn.drawSVG = function(options) {
      var settings = $.extend({
        color: '#556b2f',
        strokeWidth: 11,
        fill: 'none',
        duration: 5
      }, options);

      return this.each(function(index, path) {
        path.setAttribute('stroke', settings.color);
        path.setAttribute('fill', settings.fill);
        path.setAttribute('stroke-width', settings.strokeWidth);
          
        path.setAttribute('stroke-linecap', 'square'); 
          // butt, round, or square
        path.setAttribute('stroke-linejoin', 'round'); 
          // miter, round or bevel

        var length = path.getTotalLength();
        // Clear any previous transition
        path.style.transition = path.style.WebkitTransition = 'none';
        // Set up the starting positions
        path.style.strokeDasharray = length;
        path.style.strokeDashoffset = length;
        // Trigger a layout so styles are calculated & the browser
        // picks up the starting position before animating
        path.getBoundingClientRect();
        // Define our transition
        path.style.transition = path.style.WebkitTransition = 'stroke-dashoffset ' + settings.duration + 's';
        // Go!
        path.style.strokeDashoffset = '0';
      });
    } 
  }(jQuery));
    
  
  function handleEvent(e) {
    if (e) {
      $('#main-logo').hide();
      $('#hoodcast-logo path').show();
        
      $('#hoodcast-logo path').drawSVG({
        color: 'gold',
        strokeWidth: 11,
        fill: 'none',
        duration: 5
      });
    }
  }
    
  function handleKeyEvent(e) {
    if (e.code === 'Enter') {
      $('#hoodcast-logo path').show();
      $('#main-logo').hide();
      $('#hoodcast-logo path').drawSVG({
        color: 'gold',
        strokeWidth: 11,
        fill: 'none',
        duration: 5
      });
    }
  }

  document.getElementById('hoodcast-search-button').addEventListener('mousedown', handleEvent);
  document.getElementById('hoodcast-search-button').addEventListener('keydown', handleKeyEvent);
  document.getElementById('enter-event1').addEventListener('keydown', handleKeyEvent);
  document.getElementById('enter-event2').addEventListener('keydown', handleKeyEvent);
});
