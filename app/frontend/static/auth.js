$(document).ready(function () {
    const accessToken = localStorage.getItem("accessToken");
    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            if (!accessToken) {
                xhr.abort();
                
                Swal.fire({
                    icon: 'error',
                    title: 'Error',
                    text: 'You are not authenticated. Please log in.',
                }).then(() => {
                    window.location = '/login';
                });
                return false;
            } else {
                xhr.setRequestHeader('Authorization', 'Bearer ' + accessToken);
            }
        }
    });

    $("#logout").click(function () {
        localStorage.removeItem("accessToken");
        window.location = "/login";
    });
});