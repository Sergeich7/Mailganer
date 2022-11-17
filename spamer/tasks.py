from project.celery import app
from django.template import Context, Template
from django.core.mail import send_mail


@app.task
def send_one_mail(
        text_templ: str, html_templ: str,
        name: str, email: str) -> bool:

    sender = 'Spamer <spamer@spam.com>'
    to = (email,)
    title = 'SPAM'
    # Вставляем переменные в шаблоны
    text_message = Template(text_templ).\
        render(Context({'Name': name, 'Email': email}))
    html_message = Template(html_templ).\
        render(Context({'Name': name, 'Email': email}))
    # Отправляем письмо
    return send_mail(
        title,
        text_message,
        sender,
        to,
        fail_silently=False,
        html_message=html_message
    )
