var speaker;
var voise_results_dict = {
    101: 'Введённые пароли не совпадают.',
    102: 'Введённое имя пользователя уже использовано.',
    103: 'Введённая электронная почта уже использована.',
    104: 'Введённые данные не корректны.',
    105: 'Вы уже вошли в систему.',
    106: 'Пользователь не найден.',
    107: 'Неверный пароль.',
    108: 'Вам необходимо подтвердить электронную почту.',
    109: 'Введённая дата не корректна.',
    110: 'Введённые параметры уведомления не корректны.',
    111: 'Заметка не найдена.',
    112: 'Тип сортировки не корректен.',
}

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
    if (result in voise_results_dict){
        voice_text(voise_results_dict[result]);
    }
    else
    {
        voice_text('Ключ ошибки не найден.');
    }
};