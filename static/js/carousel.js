//Add the first image 

$(document).ready(function(){


    //initializations
    var pictures = $("#slider").children("li");
    var navItems = $("#navigation").children("li");
    var currentNav, currentPic;


    //initialize nav
    $("#navigation").find('li').first().addClass('active');

    function goTo(i){
        $(navItems).removeClass('active');
        $("#navigation li").eq(i).addClass('active');

        pictures.fadeOut(400)
                .eq(i).fadeIn(400);
    }



    //Click on new navigation button; make active
    $("#navigation li").on('click',function(){
        var index = $(this).index();
        goTo(index);
    });

    $("#next").on('click',function(){
        //get current Nav index
        currentNav = parseInt($('.active').index());
            if (currentNav <3){
                goTo(currentNav+1);
            } else {
                goTo(0);
            }
    });

    $("#prev").on('click',function(){
        //get current Nav index
        currentNav = parseInt($('.active').index());
            if (currentNav >0){
                goTo(currentNav-1);
            } else {
                goTo(3);
            }
    });
    goTo(0);

    //loop to cycle through
    setInterval(function(){
      $("#next").trigger('click');
    },2500);
});


