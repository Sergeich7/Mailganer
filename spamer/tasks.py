from project.celery import app
from django.template import Context, Template
from django.core.mail import send_mail


@app.task
def send_one_mail(template: str, name: str, email: str) -> bool:
    sender = 'Spamer <spamer@spam.com>'
    to = (email,)
    title = 'SPAM'
    # Вставляем переменные в шаблон
    body = Template(template).\
        render(Context({'Name': name, 'Email': email}))
    # Отправляем письмо
    return send_mail(
        title,
        body,
        sender,
        to,
        fail_silently=False,
    )
