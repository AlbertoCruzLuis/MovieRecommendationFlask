function ready(fn) {
    if(document.readyState != 'loading') {
      fn();
    } else {
      document.addEventListener('DOMContentLoaded', fn);
    }
  }
  
  var selectedRating = parseInt(document.getElementById('rating-stars').getAttribute("value"));
  
  ready(function(){
  
    function addClass(el, className) {
      if(typeof el.length == "number") {
        Array.prototype.forEach.call(el, function(e,i){ addClass(e, className) });
        return;
      }
      if (el.classList)
        el.classList.add(className);
      else
        el.className += ' ' + className;    
    }
    function removeClass(el, className) {
      if(typeof el.length == "number") {
        Array.prototype.forEach.call(el, function(e,i){ removeClass(e, className) });
        return;
      }
      if (el.classList)
        el.classList.remove(className);
      else if(el.className)
        el.className = el.className.replace(new RegExp('(^|\\b)' + className.split(' ').join('|') + '(\\b|$)', 'gi'), ' ');
    }
  
    var stars = document.querySelectorAll(".rating-stars a");
    Array.prototype.forEach.call(stars, function(el, i){
      // el.addEventListener("mouseover", function(evt){
      //   removeClass(stars, "selected");
      //   // For each star up to the highlighted one, add "hover"
      //   var to = parseInt(evt.target.getAttribute("data-rating"));
      //   Array.prototype.forEach.call(stars, function(star, i) {
      //     if(parseInt(star.getAttribute("data-rating")) <= to) {
      //       addClass(star, "hover");
      //     }
      //   });
      // });
      // el.addEventListener("mouseout", function(evt){
      //   removeClass(evt.target, "hover");
      // });
      el.addEventListener("click", function(evt){
        selectedRating = parseInt(evt.target.getAttribute("data-rating"));
        removeClass(stars, "selected");
        Array.prototype.forEach.call(stars, function(star, i) {
          if(parseInt(star.getAttribute("data-rating")) <= selectedRating) {
            addClass(star, "selected");
          }
        });      
        evt.preventDefault();
      });
    });
    document.querySelector(".rating-stars").addEventListener("mouseout", function(evt){
      // When the cursor leaves the whole rating star area, remove the "hover" class and apply 
      // the "selected" class to the number of stars selected.
      removeClass(stars, "hover");
      if(selectedRating) {
        Array.prototype.forEach.call(stars, function(star, i) {
          if(parseInt(star.getAttribute("data-rating")) <= selectedRating) {
            addClass(star, "selected");
          }
        });      
      }
    });
    
  });