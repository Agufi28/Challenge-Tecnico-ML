$(function () {
	function login(page, username, password) {
		$.ajax({
			type: 'POST',
			url: page,
			data: $.param({
				username: username,
				password: password
			}),
			contentType: "application/x-www-form-urlencoded",
			cache: false,
			success: function (response) {
				localStorage.setItem('accessToken', response.access_token);

				window.location = '/databases'
			},
			error: function (response, e, n) {
				Swal.fire({
					icon: 'error',
					title: 'Error',
					text: response.responseJSON.detail
				});
			}
		});
	}

	$("form").submit(function (e) {
		e.preventDefault();
		var username_val = $("#username").val();
		var password_val = $("#password").val();

		if (username_val == '' || password_val == '') {
			Swal.fire({
				icon: 'warning',
				title: 'Oops...',
				text: 'Username or password is empty',
			});
		} else {
			login(`/api/v1/token`, username_val, password_val);
		}
	});
});