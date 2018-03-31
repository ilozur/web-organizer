var speaker;

function init_speechkit()
{
    speaker = new ya.speechkit.Tts(
    {
        apikey: '762b9ab5-635c-4142-b8bd-9aca7274f427',
        emotion: 'neutral',
        speed: 1,
        speaker: 'jane',
        lang: 'ru-RU'
    });
};

function voice_text(text, special_callback=null)
{
    speaker.speak(text, { stopCallback: special_callback });
};

function voice_ajax_result(result)
{
    if (result == '101')
    {
        voice_text('Введённые пароли не совпадают.');
    }
    else if (result == '102')
    {
        voice_text('Введённое имя пользователя уже использовано.');
    }
    else if (result == '103')
    {
        voice_text('Введённая электронная почта уже использована.');
    }
    else if (result == '104')
    {
        voice_text('Введённые данные не корректны.');
    }
    else if (result == '105')
    {
        voice_text('Вы уже вошли в систему.');
    }
    else if (result == '106')
    {
        voice_text('Пользователь не найден.');
    }
    else if (result == '107')
    {
        voice_text('Неверный пароль.');
    }
    else if (result == '108')
    {
        voice_text('Вам необходимо подтвердить электронную почту.');
    }
    else if (result == '109')
    {
        voice_text('Введённая дата не корректна.');
    }
    else if (result == '110')
    {
        voice_text('Введённые параметры уведомления не корректны.');
    }
    else if (result == '111')
    {
        voice_text('Заметка не найдена.');
    }
    else if (result == '112')
    {
        voice_text('Тип сортировки не корректен.')
    }
};