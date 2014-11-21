$(document).ready(function() {
        $('.dropdown_box').submit(function(event) {
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
    document.form["11"].checked

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
    }