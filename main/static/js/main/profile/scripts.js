function get_user_data()
{
	$.ajax({
		type: "POST",
		url: '/userprofile/get_user_data',
		success: function(response)
		{
			$('#id_name').val(response['user'].name);
			$('#id_email').val(response['user'].email);
			$('#id_surname').val(response['user'].surname);
			$('#name').html(response['user'].name);
			$('#email').html(response['user'].email);
			$('#surname').html(response['user'].surname);
			$('#username').html(response['user'].username);
			$("#change_password_form").find(':input').each(function(){
				$(this).removeAttr('disabled');
			});
			$('#change_password_btn').removeAttr('disabled');
		}
	});
};

function change_password()
{
	form_data = $('#change_password_form').serialize();
	$("#change_password_form").find(':input').each(function(){
		$(this).attr('disabled', 'disabled');
	});
	$('#change_password_btn').attr('disabled', 'disabled');
	$.ajax({
		type: "POST",
		url: '/userprofile/change_password',
		data: form_data,
		success: function(response)
		{
			if (response['result'] == 'Success')
			{
				location.href = "/siteprofile"
			}
			else
			{
				alert(response['result']);
			}
			$("#change_password_form").find(':input').each(function(){
				$(this).removeAttr('disabled');
			});
			$('#change_password_btn').removeAttr('disabled');

		}
	});
};
function change_user_data()
{
	form_data = $('#change_user_data_form').serialize();
	$("#change_user_data_form").find(':input').each(function(){
		$(this).attr('disabled', 'disabled');
	});
	$('#save_changes_btn').attr('disabled', 'disabled');
	$.ajax({
		type: "POST",
		url: '/userprofile/change_user_data',
		data: form_data,
		success: function(response)
		{
			alert(response['answer']);
			$("#change_user_data_form").find(':input').each(function(){
				$(this).removeAttr('disabled');
			});
			$('#save_changes_btn').removeAttr('disabled');
		}
	});
};
function upload_avatar()
{
	form_data = $('#upload_file_form').serialize();
	$("#upload_file_form").find(':input').each(function(){
		$(this).attr('disabled', 'disabled');
	});
	$('#save_changes_btn').attr('disabled', 'disabled');
	$.ajax({
		type: "POST",
		url: '/userprofile/upload_avatar',
		data: form_data,
		success: function(response)
		{
			$('#save_changes_btn').removeAttr('disabled');
		}
	});
};
