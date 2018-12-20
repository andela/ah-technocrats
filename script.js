function showMenu() {
            
    let menu = document.getElementById("menu-toggle")
    if (menu.style.display === "none") {
        menu.style.display = "block";
    } else {
        menu.style.display = "none";
    }
        
    }

$('#toggle').click(function(){
    $('.sidebar').sidebar('toggle');
});

$('.ui.radio.checkbox')
  .checkbox()
;


$('.ui.sidebar').sidebar({
    context: $('.bottom.segment')
  })
  .sidebar('attach events', '.menu .item');

$('.ui.rating')
  .rating()
;
try {
    var simplemde = new SimpleMDE();
    simplemde.value("This text will appear in the editor");
}catch (e) {

}
try {
    $('.paragraph').quoteShare()
}catch (e) {
  console.log(e);
}

$('.ui.dropdown')
  .dropdown({
    action: 'combo'
  })
;

// $('.ui.modal')
//   .modal({
//     closable  : false,
//     onDeny    : function(){
//       window.alert('Wait not yet!');
//       return false;
//     },
//     onApprove : function() {
//       window.alert('Approved!');
//     }
//   })
//   .modal('show')
// ;

// $('#search').click(function(){
//   $('.ui.modal')
//   .modal('show')
// ;
// });

$('.ui.modal')
  .modal('show')
;


// Favorite Button - Heart
$('.fav_me').click(function() {
    $(this).toggleClass('active');
});

/* when a user clicks, toggle the 'is-animating' class */
$(".fav_me").on('click touchstart', function(){
    $(this).toggleClass('is_animating');
});

/*when the animation is over, remove the class*/
$(".fav_me").on('animationend', function(){
    $(this).toggleClass('is_animating');
});

