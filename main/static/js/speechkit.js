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
}

function hello_user(user_name)
{
    speaker.speak("Добрый день, " + user_name + "!");
};