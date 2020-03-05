
function hover_objective_cards() {
  // Find the associated objective card id
  var objId = $(this).find("a").attr("name");
  var selectedObj = document.getElementById(objId);

  // Find the previously selected objective card (if applicable)
  var prevSelectedObj = $('.selected--objective-card__content')[0];

  // Display the text in the newly selected card and hide it in the previously selected one
  if(selectedObj.className != 'selected--objective-card__content' && prevSelectedObj){
        prevSelectedObj.className = 'objective-card__content';
        selectedObj.className = 'selected--objective-card__content';
  }
  if(selectedObj.className != 'selected--objective-card__content'){
        selectedObj.className = 'selected--objective-card__content';
  }
}

$('.objective-choice').on("click", hover_objective_cards);
