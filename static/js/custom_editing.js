
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

        $('.btn-primary').submit(function(event) {
            event.preventDefault();
                getNotifications();
        });
    });

    document.form["1"].checked = true,
    document.form["2"].checked,
    document.form["3"].checked,
    document.form["4"].checked,
    document.form["5"].checked,
    document.form["6"].checked,
    document.form["7"].checked,
    document.form["8"].checked,
    document.form["9"].checked,
    document.form["10"].checked,
    document.form["11"].checked;

    getNotifications();

    function getNotifications() {
        var formData = {
            'getAllNotifications': 1,
            '1'         : document.form["1"].checked,
            '2'         : document.form["2"].checked,
            '3'         : document.form["3"].checked,
            '4'         : document.form["4"].checked,
            '5'         : document.form["5"].checked,
            '6'         : document.form["6"].checked,
            '7'         : document.form["7"].checked,
            '8'         : document.form["8"].checked,
            '9'         : document.form["9"].checked,
            '10'        : document.form["10"].checked,
            '11'        : document.form["11"].checked
        };

        $.ajax({
            url     : '/editlang',
            type    : 'post',
            data    : formData,
            success :function(response) {
                    alert(response);

            },
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


