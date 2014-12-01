
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

    $('.edit-parent').editable('/parent_wksht', {
     type      : 'textarea',
     cancel    : 'Cancel',
     submit    : 'OK',
     indicator : '<img src="img/indicator.gif">',
     tooltip   : 'Click to edit...',
     // id        : 'id',
     // name      : 'name',
     // data      : "data"
 });

    $('.type-dropdown').change(function() {
        var clicked_id = $(".type-dropdown option:selected").val();

        $.ajax({
          type: "POST",
          url: '/edittype',
          data: {id: clicked_id}
      });
     });



    $('table td.del').click(function() {
        var self = this;
        $.ajax({
          type: "POST",
          url: '/delete_daycare',
          data: {wkshtid: $(self).attr("data")},
          success: function(data) {
            if (data=="OK") {
                $(self).parent().remove();
            }
          }
        });
    });

    });






