from project.celery import app
from django.template import Context, Template
from django.core.mail import send_mail

@app.task
def send_one_mail(template, name, email):
    sender = 'Spamer <spamer@spam.com>'
    to = (email,)
    title = 'SPAM'
    body = Template(template).\
        render(Context({'Name': name, 'Email': email}))
    return send_mail(
        title,
        body,
        sender,
        to,
        fail_silently=False,
    )

