// Div which contains the features
var featureDiv = document.getElementById('landing-feature');
// Path to background images
var bkgs = {
    'landing-feature-txt-dev': 'img-3-feature-developer.png',
    'landing-feature-txt-pla': 'img-4-feature-planner.png',
    'landing-feature-txt-cit': 'img-10-feature-citizen.png'
};

// Set the preselected background
featureDiv.style.backgroundImage = "url('static/img/img-3-feature-developer.png')";

$('.opt-title').on("mouseover", function() {
  // Find the associated feature id
  var ftId = $(this).find("a").attr("href").substring(1);
  var tabContents = document.getElementById(ftId);
  // Change the background image
  featureDiv.style.backgroundImage = "url('static/img/" + bkgs[ftId] + "')";
  // Find the previously selected tab
  var prevSelectedTab = $('.selected--opt--content')[0];
  // Select the new tab and deselect the previously selected
  if(tabContents.className != 'selected--opt--content' && prevSelectedTab){
        prevSelectedTab.className = 'opt--content';
        tabContents.className = 'selected--opt--content';
  }
  else{
       tabContents.className = 'selected--opt--content';
  }
});
