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



$('.ui.sidebar').sidebar({
    context: $('.bottom.segment')
  })
  .sidebar('attach events', '.menu .item');

$('.ui.rating')
  .rating()
;
try {
    var simplemde = new SimpleMDE();
}catch (e) {

}

$('.ui.dropdown')
  .dropdown({
    action: 'combo'
  })
;

$('.ui.modal')
  .modal({
    closable  : false,
    onDeny    : function(){
      window.alert('Wait not yet!');
      return false;
    },
    onApprove : function() {
      window.alert('Approved!');
    }
  })
  .modal('show')
;

