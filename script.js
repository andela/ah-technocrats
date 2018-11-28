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

