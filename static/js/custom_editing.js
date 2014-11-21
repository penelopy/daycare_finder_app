
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

    // $('.type-dropdown-search').change(function() {
    //     var clicked_id = $(".type-dropdown option:selected").val();

    // // $.post("/edittype", function(this.id) {
    //     console.log(clicked_id);
    //     $.ajax({
    //       type: "POST",
    //       url: '/processtype',
    //       data: {id: clicked_id}
    //   });
    // });

// $('.checkbox').checked(function) { 
//     var checked_box_id = $(".checkbox").val():
//     $.ajax({
//         type: "POST",
//         url: '/process_adv_search',
//         data: {id: checked_box_id}
//     });
// });

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

    makeEditable("edit-area", "divOne", "about_us"); 
    makeEditable("edit-area", "divTwo", "neighborhood");
    makeEditable("edit-area", "divThree", "hours");
    makeEditable("edit-area", "divFour", "capacity");
    makeEditable("edit-area", "divFive", "primary_contact");
    makeEditable("edit-area", "divSix", "license_num");
    makeEditable("edit-area", "divSeven", "phone");
    makeEditable("edit-area", "divEight", "email");
    makeEditable("edit-area", "divNine", "website");
    makeEditable("edit-area", "divTen", "fburl");
});


