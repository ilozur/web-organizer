var background_listener;
var key_phrases;
var listening_mode;

function start_background_listening(language)
{
    if (annyang)
    {
        var commands = {};
        if (language == "ru")
        {
            commands = {
                "привет (ева)": function() { alert('Ева'); },
                "открой заметки": function() { window.location.href = "/notes"; },
                "открой главную": function() { window.location.href = "/"; },
                "открой календарь": function() { window.location.href = "/calendar"; },
                "открой напоминания": function() { window.location.href = "/todo"; },
            };
        }
        else if (language == "en")
        {
            commands = {
                "hello (eva)": function() { alert('Eva'); },
            };
        }
        else
        {
            alert('Your language is unsupported');
        }
        annyang.debug();
        annyang.setLanguage(language);
        annyang.addCommands(commands);
        annyang.start();
    }
    else
    {
        alert('Your browser is unsupported for voice. Sorry');
    }
};