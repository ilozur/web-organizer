$(document).ready(function(){
    $(window).scroll(function(){
        if ($(this).scrollTop() > 100) {
            $('.scrollup').fadeIn();
        } else {
            $('.scrollup').fadeOut();
        }
    });
    $('.scrollup').click(function(){
        $("html, body").animate({ scrollTop: 0 }, 600);
        return false;
    });
});

$(document).ready(function() {
   $('a[href^="#"]').click(function () {
     elementClick = $(this).attr("href");
     destination = $(elementClick).offset().top;
     if($.browser.safari){
       $('body').animate( { scrollTop: destination }, 1200 );
     }else{
       $('html').animate( { scrollTop: destination }, 1200 );
     }
     return false;
   });
});

$(document).ready(function() {
    $(window).on('scroll', function() {
        var scroll = $(window).scrollTop();
        if (scroll >= 50) {
            $('#header').addClass('fixed');
        } else {
            $('#header').removeClass('fixed');
        }
    });
});

function sign_in_ajax()
{
    form_data = $('#sign_in_form').serialize();
    $("#sign_in_form").find(':input').each(function(){
        $(this).attr('disabled', 'disabled');
    });
    $('#sign_in_btn').attr('disabled', 'disabled');
    $("#sign_up_form").find(':input').each(function(){
        $(this).attr('disabled', 'disabled');
    });
    $('#sign_up_btn').attr('disabled', 'disabled');
    $.ajax({
        type: "POST",
        url: '/sign_in/',
        data: form_data,
        success: function(response)
        {
            if (response['result'] == "100")
            {
                voice_text('Добро пожаловать!', function(){ window.location.href = '/'; });
            }
            else
            {
                voice_ajax_result(response['result']);
                $("#sign_in_form").find(':input').each(function(){
                   $(this).removeAttr('disabled');
                });
                $('#sign_in_btn').removeAttr('disabled');
                $("#sign_up_form").find(':input').each(function(){
                    $(this).removeAttr('disabled');
                });
                $('#sign_up_btn').removeAttr('disabled');
            }
        }
    });
};

function sign_up_ajax()
{
    form_data = $('#sign_up_form').serialize();
    $("#sign_up_form").find(':input').each(function(){
        $(this).attr('disabled', 'disabled');
    });
    $('#sign_up_btn').attr('disabled', 'disabled');
    $("#sign_in_form").find(':input').each(function(){
        $(this).attr('disabled', 'disabled');
    });
    $('#sign_in_btn').attr('disabled', 'disabled');
    $.ajax({
        type: "POST",
        url: '/sign_up/',
        data: form_data,
        success: function(response)
        {
            if (response['result'] == "100")
            {
                voice_text('Вы успешно зарегестрировались. Вам отправлено письмо для подтверждения почты.', function(){ window.location.href = '/'; });
            }
            else
            {
                voice_ajax_result(response['result']);
                $("#sign_up_form").find(':input').each(function(){
                $(this).removeAttr('disabled');
                });
                $('#sign_up_btn').removeAttr('disabled');
                $("#sign_in_form").find(':input').each(function(){
                   $(this).removeAttr('disabled');
                });
                $('#sign_in_btn').removeAttr('disabled');
            }
        }
    });
};


function create_recover_key()
{
    $("#sign_up_form").find(':input').each(function(){
        $(this).attr('disabled', 'disabled');
    });
    $('#sign_up_btn').attr('disabled', 'disabled');
    $("#sign_in_form").find(':input').each(function(){
        $(this).attr('disabled', 'disabled');
    });
    $('#sign_in_btn').attr('disabled', 'disabled');
    form_data = $('#recover_password_form').serialize();
    $("#recover_password_form").find(':input').each(function(){
        $(this).attr('disabled', 'disabled');
    });
    $('#recover_password_btn').attr('disabled', 'disabled');
    $.ajax({
        type: "POST",
        url: '/siteprofile/recover_password_key',
        data: form_data,
        success: function(response)
        {
            if (response['result'] == "100")
            {
                voice_text('Вам отправлено письмо для восствновления пароля.', function(){ window.location.href = '/'; });
            }
            else
            {
                voice_ajax_result(response['result']);
            }
            $("#sign_up_form").find(':input').each(function(){
            $(this).removeAttr('disabled');
            });
            $('#sign_up_btn').removeAttr('disabled');
            $("#sign_in_form").find(':input').each(function(){
               $(this).removeAttr('disabled');
            });
            $('#sign_in_btn').removeAttr('disabled');
            $("#recover_password_form").find(':input').each(function(){
               $(this).removeAttr('disabled');
            });
            $('#recover_password_btn').removeAttr('disabled');
        }
    });
};