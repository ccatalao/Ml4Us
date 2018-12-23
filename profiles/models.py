from django.conf import settings
from django.db import models
from django.core.mail import send_mail
from django.urls import reverse


User = settings.AUTH_USER_MODEL


class Profile(models.Model):
    user              = models.OneToOneField(User, on_delete=models.CASCADE) # user.profile
    activation_key    = models.CharField(max_length=120, blank=True, null=True)
    activated         = models.BooleanField(default=True)
    timestamp         = models.DateTimeField(auto_now_add=True)
    updated           = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.username

    def send_activation_email(self):
        if not self.activated:
            self.activation_key = code_generator()# 'somekey' #gen key
            self.save()
            path_ = reverse('activate', kwargs={"code": self.activation_key})
            full_path = "https://carloscatalao.com" + path_
            subject = 'Activate Account'
            from_email = settings.DEFAULT_FROM_EMAIL
            message = f'Activate your account here: {full_path}'
            recipient_list = [self.user.email]
            html_message = f'<p>Activate your account here: {full_path}</p>'
            print(html_message)
            sent_mail = send_mail(
                            subject, 
                            message, 
                            from_email, 
                            recipient_list, 
                            fail_silently=False, 
                            html_message=html_message)
            sent_mail = False
            return sent_mail


