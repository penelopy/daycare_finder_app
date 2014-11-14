
$(document).ready(function() {
     $('.edit-area').editable('/edit_center', {
         type      : 'textarea',
         cancel    : 'Cancel',
         submit    : 'OK',
         indicator : '<img src="img/indicator.gif">',
         tooltip   : 'Click to edit...',
         id        : 'id',
         name      : 'name'
     });



var makeEditable = function(divClass, id, name) {

    $('.' + divClass).editable('/edit_center', {
         type      : 'textarea',
         cancel    : 'Cancel',
         submit    : 'OK',
         indicator : '<img src="img/indicator.gif">',
         tooltip   : 'Click to edit...',
         id        : id,
         name      : name
     });
};


makeEditable("edit-area", "divOne", "about_us"); // -> <div class="1"><input type="textarea" name="nameEdit" id="divOne"></input></div> 
// makeEditable("2", "divThree", "locationEdit")
// makeEditable("3", "divTwo", "hoursEdit")

});

