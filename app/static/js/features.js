// Div which contains the features
var featureDiv = $("#landing-feature");
// Path to background images
var bkgs = {
    'landing-feature-txt-dev': 'img-3-feature-developer.png',
    'landing-feature-txt-pla': 'img-4-feature-planner.png',
    'landing-feature-txt-cit': 'Image_gray.svg'
};

// Set the preselected background
featureDiv.css('background-image', "url('static/img/img-3-feature-developer.png')");

var fade1 = 0.2;
var fade2 = 1.5;


function apply_select(feature_type){
    //change class to selected
    var ftId = 'landing-feature-' + feature_type + '-btn';
    var ft = document.getElementById(ftId).getElementsByClassName('landing-feature__img')[0];
    ft.className = 'landing-feature__img ' + 'selected';
    ft = document.getElementById(ftId).getElementsByClassName('landing-feature__description')[0];
    ft.className = 'landing-feature__description ' + 'selected';
}

function apply_deselect(feature_type){
    //change class to deselected by removing selected class
    var ftId = 'landing-feature-' + feature_type + '-btn';
    var ft = document.getElementById(ftId).getElementsByClassName('landing-feature__img')[0];
    ft.className = 'landing-feature__img';
    ft = document.getElementById(ftId).getElementsByClassName('landing-feature__description')[0];
    ft.className = 'landing-feature__description';
}

function hover_features() {
  // Find the associated feature id
  var ftId = $(this).find("a").attr("name").replace("link-", "");
  var ftType = ftId.split('-').pop();
  var selectedTab = document.getElementById(ftId);

  // Change the background image
  featureDiv.fadeTo('slow', fade1, function(){
    $(this).css('background-image', "url('static/img/" + bkgs[ftId] + "')");
  }).fadeTo('slow', fade2);
  // Find the previously selected tab
  var prevSelectedTab = $('.selected--opt--content')[0];
  var prevFtId = prevSelectedTab.id
  var prevftType = prevFtId.split('-').pop();

  // Select the new tab and deselect the previously selected
  if(selectedTab.className != 'selected--opt--content' && prevSelectedTab){
        prevSelectedTab.className = 'opt--content';
        apply_deselect(prevftType);
        selectedTab.className = 'selected--opt--content';
        apply_select(ftType);
  }
}

$('.landing-feature__img').on("click", hover_features);
$('.landing-feature__description').on("click", hover_features);

$('.feature-next').on("click", function() {
  // Find the currently selected tab
  var selectedTab = $('.selected--opt--content')[0];
  var selectedId = selectedTab.id.slice(-3);
  // Infer the next tab form the current id
  var nextId = '';
  if (selectedId == 'dev'){
    nextId = 'pla';
  }
  else if (selectedId == 'pla'){
    nextId = 'cit';
  }
  else if (selectedId == 'cit'){
    nextId = 'dev';
  }
  // update "selected" class
  apply_deselect(selectedId);
  apply_select(nextId);

  nextId = selectedTab.id.replace(selectedId, nextId)
  var nextTab = document.getElementById(nextId);

  // Change the background image
  featureDiv.fadeTo('slow', fade1, function(){
    $(this).css('background-image', "url('static/img/" + bkgs[nextId] + "')");
  }).fadeTo('slow', fade2);

  // Select the new tab and deselect the previously selected
  selectedTab.className = 'opt--content';
  nextTab.className = 'selected--opt--content';

});


$('.feature-previous').on("click", function() {
  // Find the currently selected tab
  var selectedTab = $('.selected--opt--content')[0];
  var selectedId = selectedTab.id.slice(-3);
  // Infer the previous tab form the current id
  var prevId = '';
  if (selectedId == 'dev'){
    prevId = 'cit';
  }
  else if (selectedId == 'pla'){
    prevId = 'dev';
  }
  else if (selectedId == 'cit'){
    prevId = 'pla';
  }
  // update "selected" class
  apply_deselect(selectedId);
  apply_select(prevId);

  prevId = selectedTab.id.replace(selectedId, prevId)
  var prevTab = document.getElementById(prevId);

  // Change the background image
  featureDiv.fadeTo('slow', fade1, function(){
    $(this).css('background-image', "url('static/img/" + bkgs[prevId] + "')");
  }).fadeTo('slow', fade2);
  // Select the new tab and deselect the previously selected
  selectedTab.className = 'opt--content';
  prevTab.className = 'selected--opt--content';
});