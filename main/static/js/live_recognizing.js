var background_listener;
var key_phrases;
var listening_mode;

function start_background_listening()
{
    init_background_listener();
};

function init_background_listener()
{
    key_phrase = 'ева';
    listening_mode = 'waiting_appeal';
    background_listener = new ya.speechkit.SpeechRecognition();
    background_listener.start({
        apikey: '762b9ab5-635c-4142-b8bd-9aca7274f427',
        dataCallback: function (text) {
            if (text.split(' ').indexOf(key_phrase) != -1)
            {
                if (listening_mode == 'waiting_appeal')
                {
                    listening_mode = 'listening_details';
                    background_listener.stop();
                    detail_listening();
                }
            }
        },
        model: 'queries',
        particialResults: true,
        utteranceSilence: 10,
    });
};

function detail_listening()
{
    window.ya.speechkit.settings.apikey = '762b9ab5-635c-4142-b8bd-9aca7274f427';
    ya.speechkit.recognize({
    doneCallback: function(text) {
        if (listening_mode == 'listening_details')
        {
            listening_mode = 'waiting_appeal';
            console.log("Финальный результат распознавания: " + text);
            background_listener.start({
                apikey: '762b9ab5-635c-4142-b8bd-9aca7274f427',
                dataCallback: function (text) {
                    if (text.split(' ').indexOf(key_phrase) != -1)
                    {
                        if (listening_mode == 'waiting_appeal')
                        {
                            listening_mode = 'listening_details';
                            background_listener.stop();
                            detail_listening();
                        }
                    }
                },
                model: 'queries',
                particialResults: true,
                utteranceSilence: 10,
            });
        }
    },
    initCallback: function () {
        console.log("Процесс распознавания команды запущен.");
    },
    utteranceSilence: 200,
});
};