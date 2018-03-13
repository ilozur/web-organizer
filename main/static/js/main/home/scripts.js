var notes_link;

function setup_link(link)
{
    notes_link = link;
};

function add_note_ajax()
{
    for (instance in CKEDITOR.instances) {
        CKEDITOR.instances[instance].updateElement();
    }
    var data = CKEDITOR.instances.id_data.getData();
    form_data = $('#add_note_form').serialize();
    form_data['data'] = data;
    $.ajax({
        type: "POST",
        url: '/notes/add',
        data: form_data,
        success: function(response)
        {
            if (response['result'] == "Success")
            {
                alert('OK, note was added');
                var now_notes_count = $("#last_notes_holder").find('p').length - 1;
                if (now_notes_count == -1)
                {
                    $("#last_notes_holder").html('<p class="lead"> <small><a href="' + notes_link + '">Показать все</a></small></p>');
                    $("#last_notes_holder").parent().find('h5').remove();
                }
                if (now_notes_count < 3)
                {
                    var new_note_html = '<p class="lead"> <a href="#" data-toggle="modal" data-target="#Open-Note">' + response["name"] + '</a></p>';
                    $("#last_notes_holder").html(new_note_html + $("#last_notes_holder").html());
                }
                else
                {
                    $("#last_notes_holder").find('p')[2].remove();
                    var new_note_html = '<p class="lead"> <a href="#" data-toggle="modal" data-target="#Open-Note">' + response["name"] + '</a></p>';
                    $("#last_notes_holder").html(new_note_html + $("#last_notes_holder").html());
                }
                $("#close_note_btn").trigger("click");
            }
        }
    });
};

function add_event_ajax()
{
    for (instance in CKEDITOR.instances) {
        CKEDITOR.instances[instance].updateElement();
    }
    var data = CKEDITOR.instances.id_description.getData();
    form_data = $('#add_event_form').serialize();
    form_data['data'] = data;
    $.ajax({
        type: "POST",
        url: '/calendar/events/add',
        data: form_data,
        success: function(response)
        {
            if (response['result'] == "success")
            {
                alert('OK, event was added');
                $("#close_calendar_btn").trigger("click");
            }
        }
    });
};