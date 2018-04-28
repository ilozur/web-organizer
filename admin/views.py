from django.shortcuts import render


def index(request):
    context = {}
    return render(request, "admin/index.html", context)

def sign_up_ajax(request):
  
    context = {}
    if request.method == "GET":
        if not request.user.is_superuser:
            context['title'] = "Sign up page"
            context['header'] = "Sign up page header"
            sign_up_form = SignUpForm()
            context['sign_up_form'] = sign_up_form
            return render(request, "main/sign_up.html", context)
        else:
            return HttpResponseRedirect('/')
    else:
        response_data = {}
        if not request.user.is_superuser:
            form = SignUpForm(request.POST)
            if form.is_valid():
                email = form.data['email'].lower()
                username = form.data['username'].lower()
                name = form.data['name']
                surname = form.data['surname']
                pass1 = form.data['password1']
                pass2 = form.data['password2']
                email_uniq = check_email_uniq(email)
                username_uniq = check_username_uniq(username)
                if email_uniq:
                    if username_uniq:
                        if pass1 == pass2:
                            user = User(email=email, username=username, first_name=name, last_name=surname, is_active=0)
                            user.set_password(pass1)
                            user.save()
                            # here should be lang=*lang taken from registration*
                            lang = Language(user=user)
                            lang.save()
                            sign_up_key = create_unic_key(user, username, pass1)
                            sign_up_key.save()
                            mail = create_mail(user,
                                               "Go to this link to activate your account: 127.0.0.1:8000/activate/" +
                                               sign_up_key.key,
                                               "<a href='http://127.0.0.1:8000/activate/" + sign_up_key.key +
                                               "'>Go to this link to activate your account</a>")
                            send_mail(mail)
                            result = "100"
                        else:
                            result = "101"
                    else:
                        result = "102"
                else:
                    result = "103"
            else:
                result = "104"
        else:
            result = "105"
        response_data['result'] = result
        return HttpResponse(json.dumps(response_data), content_type="application/json")
