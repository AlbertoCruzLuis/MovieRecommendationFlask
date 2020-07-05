

let rating = document.querySelectorAll(".rating");
let stars = [];
let value_rating = [];

function change_rating(value, name_rating){
  $.ajax({
    type: 'POST',
    url : '/home/rating',
    data : {'rating':value,'name_rating':name_rating},
    dataType: "json"
  }).done( function() {
    console.log( 'Success!!' );
  }).fail( function() {
      console.log( 'Error!!' );
  });
}

function get_value_rating(){
  for (let i = 0; i < rating.length; i++) {
    stars.push(rating[i].querySelectorAll("input"));
    value_rating.push(rating[i].getAttribute('value'));
  }
}

// Fill Rating get database
function rating_database(){
  for (let i = 0; i < stars.length; i++) {
    for (let j = 0; j < stars[i].length; j++) {
      if (value_rating[i]-1 >= j)
      {
        stars[i][j].style.backgroundImage = "url('/static/img/rating-star-yellow.png')";
      }
      else{
        stars[i][j].style.backgroundImage = "url('/static/img/rating-star.png')";
      }
    }
  }
}

function control_rating(i,j){
  let add = j;
  while(add >= 0){
    stars[i][add].style.backgroundImage = "url('/static/img/rating-star-yellow.png')";
    add--;
  }
  let remove = j+1;
  while(remove < 5){
    stars[i][remove].style.backgroundImage = "url('/static/img/rating-star.png')";
    remove++;
  }
}

window.onload = function()
{
  get_value_rating();
  rating_database();
  

  // Fill Rating for action user
  for (let i = 0; i < stars.length; i++) {
    for (let j = 0; j < stars[i].length; j++) {
      if (stars[i][j].onmouseover = function(){
        control_rating(i,j);
      })
      if (stars[i][j].onmouseout = function(){
        get_value_rating();
        rating_database();
      })
      if (stars[i][j].onclick = function(e){
        control_rating(i,j);
        //Post of data rating
        name_rating = rating[i].getAttribute('name');
        rating[i].setAttribute('value',j+1);
        console.log(name_rating);
        change_rating(j+1,name_rating);
      }){
      }
    }
  }
}