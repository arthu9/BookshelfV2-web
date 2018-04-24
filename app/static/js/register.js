function login() {
    $.ajax(
        {
            type: "POST",
            url: 'http://127.0.0.1:8080/signup',
            contentType: 'application/json; charset=utf-8',
            dataType: "json",
            crossDomain: true,
            data: JSON.stringify({
                username: $("#username").val(),
                password: $("#password").val()
                first_name: $("#first_name").val()
                last_name: $("#last_name").val()
                contact_number: $("#contact_number").val()
                birth_date: $("#birth_date").val()
                gender: $("#gender").val()
            }),


            error: function (data) {
                alert("error")
            },
            success: function (data) {
                if (data.status == 'ok') {
                    window.location.replace('http://www.google.com/');
                }
                else {
                    alert(data.message)
                }

            }
        });
}