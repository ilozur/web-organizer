selected_sorting_type = null;
selected_folder = null;

function init()
{
    $.each($('#note_list .list-group a'), function() { this.onclick = function() { get_note_data($(this).attr('id').split('_')[1]) } });
    $.each($('#note_folders .list-group a'), function() { this.onclick = function() { get_folder($(this).attr('id').split('_')[1]) } });
    document.getElementById('clean_search_btn').onclick = function() { $('input[name="aim"]').val(''); search(); };
    document.getElementById('add_note_btn').onclick = function() { add_note(); };
    $('input[name="aim"').on('keyup paste', function() { search(); });
};

function add_note()
{
    $('#add_note_btn').attr('disabled', '');
    $('#note_show').attr('hidden', '');
    $('#note_list .list-group p').attr('hidden', '');
    $.each($('#note_list .list-group a'), function()
    {
        if ($(this).hasClass('editing'))
        {
            save_note($(this).attr('id').split('_')[1]);
            $(this).removeClass('editing');
        }
        $(this).removeClass('active') });
    $('#note_list .list-group').html('<a id="note_adding" class="list-group-item list-group-item-action list-group-item-warning active">Новая заметка</a>' + $('#note_list .list-group').html());
    $.each($('#note_list .list-group a'), function() { this.onclick = function() { get_note_data($(this).attr('id').split('_')[1]) } });
    document.getElementById('note_adding').onclick = null;
    for (instance in CKEDITOR.instances) {
        CKEDITOR.instances[instance].updateElement();
    }
    document.getElementById('save_note_btn').onclick = function() { save_note('new_note', true); };
    CKEDITOR.instances.id_note_data.setData("");
    $('#id_note_data').val('');
    $('#note_add').removeAttr('hidden');

};

function edit_note(id)
{
    $('#note_' + id).addClass('editing');
    $('#note_show').attr('hidden', '');
    $('input[name="note_title"]').val($('#note_show h3').html());
    CKEDITOR.instances.id_note_data.setData($('#note_show p').html());
    for (instance in CKEDITOR.instances) {
        CKEDITOR.instances[instance].updateElement();
    }
    document.getElementById('save_note_btn').onclick = function() { save_note(id, true); };
    $('#note_add').removeAttr('hidden');
};
function get_folder(id)
{
    selected_folder = id;
    $.each($('#note_list .list-group a'), function() { $(this).remove(); });
    $('input[name="aim"]').val('');
    $('#clean_search_btn').attr('hidden', '');
    $('#show_folder_preloader').removeAttr('hidden');
    $.each($('#note_folders .list-group a'), function() { $(this).removeClass('active') })
    $('#folder_' + id).addClass('active');
    $.ajax({
        type: "POST",
        url: '/notes/get_folder',
        data: { "id": id, "sorting_type": selected_sorting_type },
        success: function(response)
        {
            $('#show_folder_preloader').attr('hidden', '');
            if (response['result'] == "100")
            {
                $.each($('#note_folders .list-group a'), function() { this.onclick = function() { get_folder($(this).attr('id').split('_')[1]) } });
                document.getElementById("folder_" + id).onclick = null;
                fill_notes_list(response['notes'])
            }
            else
            {
                voice_ajax_result(response['result']);
            }
        }
    });
};

function save_note(id, show_note=false)
{
    for (instance in CKEDITOR.instances) {
        CKEDITOR.instances[instance].updateElement();
    }
    var data = $('#save_note_form').serialize();
    data['note_data'] =  CKEDITOR.instances.id_note_data.getData();
    data += "&id=" + id + "&folder=" + selected_folder;
    $.ajax({
        type: "POST",
        url: '/notes/save',
        data: data,
        success: function(response)
        {
            if (response['result'] == "100")
            {
                $('#note_add').attr('hidden', '');
                if (id == "new_note")
                {
                    $('#note_adding').attr('id', 'note_' + response['id']);
                }
                $('#note_' + response['id']).html(response['title']);
                if (show_note)
                {
                    get_note_data(response['id']);
                }
            }
            else
            {
                voice_ajax_result(response['result']);
            }
        }
    });
};

function get_note_data(id)
{
    $('#note_add').attr('hidden', '');
    $('#note_show').attr('hidden', '');
    $('#show_note_preloader').removeAttr('hidden');
    $('#add_note_btn').removeAttr('disabled');
    $.each($('#note_list .list-group a'), function()
    {
        if (($(this).attr('id') == "note_adding") && ($(this).hasClass('active')))
        {
            if (CKEDITOR.instances.id_note_data.getData() == "")
            {
                $(this).remove();
            }
            else
            {
                save_note('new_note');
                $(this).removeClass('active');
            }
        }
        else
        {
            if ($(this).hasClass('editing'))
            {
                save_note($(this).attr('id').split('_')[1]);
                $(this).removeClass('editing');
            }
            $(this).removeClass('active');
        }
    });
    $('#note_' + id).addClass('active');
    $.ajax({
        type: "POST",
        url: '/notes/get_note_data',
        data: { "id": id },
        success: function(response)
        {
            $('#show_note_preloader').attr('hidden', '');
            if (response['result'] == "100")
            {
                $.each($('#note_list .list-group a'), function() { this.onclick = function() { get_note_data($(this).attr('id').split('_')[1]) } });
                document.getElementById("note_" + response['id']).onclick = null;
                set_note_show(response);
                $('#note_show').removeAttr('hidden');
            }
            else
            {
                voice_ajax_result(response['result']);
            }
        }
    });
};

function set_note_show(response)
{
    $('#note_show .note h3').html(' ' + response['title'] + ' ');
    $('#note_show .note .date').html(response['added_time']);
    $('#note_show .note .text').html(response['data']);
    $('#delete_btn').unbind('click');
    $('#delete_btn').click(function() { delete_note(response['id']); });
    document.getElementById('edit_note_btn').onclick = function() { edit_note(response['id']); };
};

function delete_note(id)
{
    var should_delete = confirm('Вы уверены?');
    if (should_delete)
    {
        $.each($('#note_list .list-group a'), function() { $(this).removeClass('active') })
        $('#note_show').attr('hidden', '');
        $.ajax({
            type: "POST",
            url: '/notes/delete',
            data: { "id": id },
            success: function(response)
            {
                if (response['result'] == "100")
                {
                    $('#note_' + id).remove();
                    if ($('#note_list .list-group a').length == 0)
                    {
                        $('#note_list .list-group p').removeAttr('hidden');
                    }
                    voice_text('Заметка удалена.');
                }
                else
                {
                    voice_ajax_result(response['result']);
                }
            }
        });
    }
};

function add_note_to_list(id, title)
{
    $('#note_list .list-group').append('<a id="note_' + id + '" class="list-group-item list-group-item-action list-group-item-warning">' + title + '</a>');
    $('#note_' + id).click(function() { get_note_data(id) } );
};

function search()
{
    if ($('input[name="aim"]').val() == "")
    {
        $('#clean_search_btn').attr('hidden', '');
    }
    else
    {
        $('#clean_search_btn').removeAttr('hidden');
    }

    $.each($('#note_list .list-group a'), function() { $(this).remove(); });
    $('#show_folder_preloader').removeAttr('hidden');
    $.ajax({
        type: "POST",
        url: '/notes/search',
        data: { "aim": $("input[name='aim']").val(), "sorting_type": selected_sorting_type, "folder": selected_folder },
        success: function(response)
        {
            $('#show_folder_preloader').attr('hidden', '');
            fill_notes_list(response['found_notes'], response['no_notes_title'])
        }
    });
};

function sort_notes(sorting_type)
{
    selected_sorting_type = sorting_type;
    $.each($('#note_list .list-group a'), function() { $(this).remove(); });
    $('#show_folder_preloader').removeAttr('hidden');
    $.ajax({
        type: "POST",
        url: '/notes/sort',
        data: { "aim": $("input[name='aim']").val(), "sorting_type": sorting_type, "folder": selected_folder },
        success: function(response)
        {
            $('#show_folder_preloader').attr('hidden', '');
            fill_notes_list(response['sorted_notes'], response['no_notes_title'])
        }
    });
};

function fill_notes_list(notes)
{
    if (notes.length == 0)
    {
        $('#note_list .list-group p').removeAttr('hidden');
    }
    for (var i = 0; i < notes.length; i++)
    {
        $('#note_list .list-group p').attr('hidden', '');
        add_note_to_list(notes[i]['id'], notes[i]['title']);
    }
};