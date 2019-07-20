from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from  .forms import ContactForm
from django.core.mail import send_mail, BadHeaderError
from backend.settings import DEFAULT_FROM_EMAIL
#from .forms import SignupForm
from django.contrib.auth.models import User
from django.core.mail import EmailMessage
from .tokens import account_activation_token
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from django.contrib.auth import login, authenticate
from django.http import JsonResponse


# Create your views here.

def index(request):
    return render(request, 'index.html', context={},)

def email(request):
    if request.method == 'GET':
        form = ContactForm()
    else:
        form = ContactForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            subject = form.cleaned_data['subject']
            from_email = form.cleaned_data['from_email']
            message1 = form.cleaned_data['message']
            mail_subject = 'Activate your account.'
            message2 = render_to_string('activate.html', {
                'user': user,
                'domain': current_site.domain,
                'uid':urlsafe_base64_encode(force_bytes(user.pk)),
                'token':account_activation_token.make_token(user),
            })
            try:
                send_mail(subject, message1, from_email, [DEFAULT_FROM_EMAIL],)
                send_mail(mail_subject ,message2, from_email, [DEFAULT_FROM_EMAIL])
            except BadHeaderError:
                return HttpResponse('Invalid header found.')
            return redirect('success')
    return render(request, "email.html", {'form': form})

def success(request):
    return HttpResponse('Success! Thank you for your message.')

def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        return HttpResponse('Thank you for your email confirmation. Now you can login your account.')
        #return JsonResponse( {'email': user.email } )
    else:
        return HttpResponse('Activation link is invalid!')



