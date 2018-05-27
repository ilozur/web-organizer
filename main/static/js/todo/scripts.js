selected_sorting_type = null;
selected_folder = null;

function init()
{
    $.each($('#todo_list .list-group a'), function() { this.onclick = function() { get_todo_data($(this).attr('id').split('_')[1]) } });
    $.each($('#todo_folders .list-group a'), function() { this.onclick = function() { get_folder($(this).attr('id').split('_')[1]) } });
    document.getElementById('clean_search_btn').onclick = function() { $('input[name="aim"]').val(''); search(); };
    document.getElementById('add_todo_btn').onclick = function() { add_todo(); };
    $('input[name="aim"]').on('keyup paste', function() { search(); });
};

function add_todo()
{
    $('#add_todo_btn').attr('disabled', '');
    $('#todo_show').attr('hidden', '');
    $('#todo_list .list-group p').attr('hidden', '');
    $.each($('#todo_list .list-group a'), function()
    {
        if ($(this).hasClass('editing'))
        {
            save_todo($(this).attr('id').split('_')[1]);
            $(this).removeClass('editing');
        }
        $(this).removeClass('active') });
    $('#todo_list .list-group').html('<a id="todo_adding" class="list-group-item list-group-item-action list-group-item-primary active">Новая задача</a>' + $('#todo_list .list-group').html());
    $.each($('#todo_list .list-group a'), function() { this.onclick = function() { get_todo_data($(this).attr('id').split('_')[1]) } });
    document.getElementById('todo_adding').onclick = null;
    document.getElementById('save_todo_btn').onclick = function() { save_todo('new_todo', true); };
    $('#id_todo_title').val('');
    $('#todo_add').removeAttr('hidden');

};

function edit_todo(id)
{
    $('#todo_' + id).addClass('editing');
    $('#todo_show').attr('hidden', '');
    $('input[name="todo_title"]').val($('#todo_show_title').html());
    document.getElementById('save_todo_btn').onclick = function() { save_todo(id, true); };
    $('#todo_add').removeAttr('hidden');
};

function get_folder(id)
{
    selected_folder = id;
    $.each($('#todo_list .list-group a'), function() { $(this).remove(); });
    $('input[name="aim"]').val('');
    $('#clean_search_btn').attr('hidden', '');
    $('#show_folder_preloader').removeAttr('hidden');
    $.each($('#todo_folders .list-group a'), function() { $(this).removeClass('active') })
    $('#folder_' + id).addClass('active');
    $.ajax({
        type: "POST",
        url: '/todo/get_folder',
        data: { "id": id, "sorting_type": selected_sorting_type },
        success: function(response)
        {
            $('#show_folder_preloader').attr('hidden', '');
            if (response['result'] == "100")
            {
                $.each($('#todo_folders .list-group a'), function() { this.onclick = function() { get_folder($(this).attr('id').split('_')[1]) } });
                document.getElementById("folder_" + id).onclick = null;
                fill_todos_list(response['todos'])
            }
            else
            {
                voice_ajax_result(response['result']);
            }
        }
    });
};

function save_todo(id, show_todo=false)
{
    var data = $('#save_todo_form').serialize();
    data += "&id=" + id + "&folder=" + selected_folder;
    $.ajax({
        type: "POST",
        url: '/todo/save',
        data: data,
        success: function(response)
        {
            if (response['result'] == "100")
            {
                $('#todo_add').attr('hidden', '');
                if (id == "new_todo")
                {
                    $('#todo_adding').attr('id', 'todo_' + response['id']);
                }
                $('#todo_' + response['id']).html(response['title']);
                if (show_todo)
                {
                    get_todo_data(response['id']);
                }
            }
            else
            {
                voice_ajax_result(response['result']);
            }
        }
    });
};

function get_todo_data(id)
{
    $('#todo_add').attr('hidden', '');
    $('#todo_show').attr('hidden', '');
    $('#show_todo_preloader').removeAttr('hidden');
    $('#add_todo_btn').removeAttr('disabled');
    $.each($('#todo_list .list-group a'), function()
    {
        if (($(this).attr('id') == "todo_adding") && ($(this).hasClass('active')))
        {
            if ($('input[name="todo_title"]'== ""))
            {
                $(this).remove();
            }
            else
            {
                save_todo('new_todo');
                $(this).removeClass('active');
            }
        }
        else
        {
            if ($(this).hasClass('editing'))
            {
                save_todo($(this).attr('id').split('_')[1]);
                $(this).removeClass('editing');
            }
            $(this).removeClass('active');
        }
    });
    $('#todo_' + id).addClass('active');
    $.ajax({
        type: "POST",
        url: '/todo/get_todo_data',
        data: { "id": id },
        success: function(response)
        {
            $('#show_todo_preloader').attr('hidden', '');
            if (response['result'] == "100")
            {
                $.each($('#todo_list .list-group a'), function() { this.onclick = function() { get_todo_data($(this).attr('id').split('_')[1]) } });
                document.getElementById("todo_" + response['id']).onclick = null;
                set_todo_show(response);
                $('#todo_show').removeAttr('hidden');
            }
            else
            {
                voice_ajax_result(response['result']);
            }
        }
    });
};

function set_todo_show(response)
{
    $('#todo_show_title').html(' ' + response['title'] + ' ');
    $('#todo_show_date').html(response['deadline']);
    $.each($('#todo_show_priority span'), function() { $(this).remove() });
    for (var i = 0; i < response['priority']; i++)
    {
        $('#todo_show_priority').append('<span class="priority">!</span>');
    }
    $('#todo_show_status').html("Статус: " + response['status'])
    $('#delete_btn').unbind('click');
    $('#delete_btn').click(function() { delete_todo(response['id']); });
    document.getElementById('edit_todo_btn').onclick = function() { edit_todo(response['id']); };
};

function delete_todo(id)
{
    var should_delete = confirm('Вы уверены?');
    if (should_delete)
    {
        $.each($('#todo_list .list-group a'), function() { $(this).removeClass('active') })
        $('#todo_show').attr('hidden', '');
        $.ajax({
            type: "POST",
            url: '/todo/delete',
            data: { "id": id },
            success: function(response)
            {
                if (response['result'] == "100")
                {
                    $('#todo_' + id).remove();
                    if ($('#todo_list .list-group a').length == 0)
                    {
                        $('#todo_list .list-group p').removeAttr('hidden');
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

function add_todo_to_list(id, title)
{
    $('#todo_list .list-group').append('<a id="todo_' + id + '" class="list-group-item list-group-item-action list-group-item-warning">' + title + '</a>');
    $('#todo_' + id).click(function() { get_todo_data(id) } );
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

    $.each($('#todo_list .list-group a'), function() { $(this).remove(); });
    $('#show_folder_preloader').removeAttr('hidden');
    $.ajax({
        type: "POST",
        url: '/todo/search',
        data: { "aim": $("input[name='aim']").val(), "sorting_type": selected_sorting_type, "folder": selected_folder },
        success: function(response)
        {
            $('#show_folder_preloader').attr('hidden', '');
            fill_todos_list(response['found_todos'], response['no_todos_title'])
        }
    });
};

function sort_todos(sorting_type)
{
    selected_sorting_type = sorting_type;
    $.each($('#todo_list .list-group a'), function() { $(this).remove(); });
    $('#show_folder_preloader').removeAttr('hidden');
    $.ajax({
        type: "POST",
        url: '/todo/sort',
        data: { "aim": $("input[name='aim']").val(), "sorting_type": sorting_type, "folder": selected_folder },
        success: function(response)
        {
            $('#show_folder_preloader').attr('hidden', '');
            fill_todos_list(response['sorted_todos'], response['no_todos_title'])
        }
    });
};

function fill_todos_list(todos)
{
    if (todos.length == 0)
    {
        $('#todo_list .list-group p').removeAttr('hidden');
    }
    for (var i = 0; i < todos.length; i++)
    {
        $('#todo_list .list-group p').attr('hidden', '');
        add_todo_to_list(todos[i]['id'], todos[i]['title']);
    }
};