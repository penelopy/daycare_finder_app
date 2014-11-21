http://stackoverflow.com/questions/24008674/ajax-form-ignoring-my-checkbox-reseting-to-default-when-submit-data

$(document).ready(function() {
        $('form').submit(function(event) {
            event.preventDefault();
                getNotifications();
        });
    });

    document.form["filterFailed"].checked = true,
    document.form["filterAlert"].checked,
    document.form["filterWarning"].checked,
    document.form["filterNotReceived"].checked,
    document.form["filterOther"].checked,
    document.form["filterSuccess"].checked


    getNotifications();

    function getNotifications() {
        var formData = {
            'getAllNotifications': 1,
            'filterFailed'       : document.form["filterFailed"].checked,
            'filterAlert'        : document.form["filterAlert"].checked,
            'filterWarning'      : document.form["filterWarning"].checked,
            'filterNotReceived'  : document.form["filterNotReceived"].checked,
            'filterOther'        : document.form["filterOther"].checked,
            'filterSuccess'      : document.form["filterSuccess"].checked
        };

        $.ajax({
            url     : 'server_script.php',
            type    : 'post',
            data    : formData,
            success :function(response) {
                    alert(response);

            },
        });
    }