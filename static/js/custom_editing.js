
$(document).ready(function() {
    console.log($('.edit-area').editable);

    $('.edit-area').editable('/edit_center', {
     type      : 'textarea',
     cancel    : 'Cancel',
     submit    : 'OK',
     indicator : '<img src="img/indicator.gif">',
     tooltip   : 'Click to edit...',
     id        : 'id',
     name      : 'name'
 });

    $('.type-dropdown').change(function() {
        var clicked_id = $(".type-dropdown option:selected").val();

        $.ajax({
          type: "POST",
          url: '/edittype',
          data: {id: clicked_id}
      });
     });

    var makeEditable = function(divClass, id, name, url) {

        $('.' + divClass).editable(url, {
         type      : 'textarea',
         cancel    : 'Cancel',
         submit    : 'OK',
         indicator : '<img src="img/indicator.gif">',
         tooltip   : 'Click to edit...',
         id        : id,
         name      : name
     });
    };


    makeEditable("edit-area", "divOne", "about_us", '/edit_center');
    makeEditable("edit-area", "divTwo", "neighborhood", '/edit_center');
    makeEditable("edit-area", "divThree", "hours", '/edit_center');
    makeEditable("edit-area", "divFour", "capacity", '/edit_center');
    makeEditable("edit-area", "divFive", "primary_contact", '/edit_center');
    makeEditable("edit-area", "divSix", "license_num", '/edit_center');
    makeEditable("edit-area", "divSeven", "phone", '/edit_center');
    makeEditable("edit-area", "divEight", "email", '/edit_center');
    makeEditable("edit-area", "divNine", "website", '/edit_center');
    makeEditable("edit-area", "divTen", "fburl", '/edit_center');
    makeEditable("edit-area", "contacted", "contacted", '/process_par_wksht');
});


