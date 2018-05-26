selected_sorting_type = null;
selected_folder = null;

function init()
{
    $.each($('#note_list .list-group a'), function() { this.onclick = function() { get_note_data($(this).attr('id').split('_')[1]) } });
    $.each($('#note_folders .list-group a'), function() { this.onclick = function() { get_folder($(this).attr('id').split('_')[1]) } });
    document.getElementById('clean_search_btn').onclick = function() { $('input[name="aim"]').val(''); search(); };
    $('input[name="aim"').on('keyup paste', function() { search(); });
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

function get_note_data(id)
{
    $('#note_show').attr('hidden', '');
    $('#show_note_preloader').removeAttr('hidden');
    $.each($('#note_list .list-group a'), function() { $(this).removeClass('active') })
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