from django.views.generic.edit import FormView
from django.urls import reverse_lazy
from django import forms
from .tasks import send_one_mail


class DataForm(forms.Form):
    mail_list = forms.CharField(label='Адресаты', widget=forms.Textarea)
    mail_templ = forms.CharField(label='Шаблон', widget=forms.Textarea)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['mail_list'].initial =\
            'Виталий|vit@yanddex.ru\nТатьяна|tan@yanddex.ru'
        self.fields['mail_templ'].initial =\
            'Привет {{Name}}!\nВаш email: {{Email}}\nМы пришлем много спама)'


class IndexView(FormView):
    template_name = 'spamer/index.html'
    form_class = DataForm
    success_url = reverse_lazy('spamer:index')

    def form_valid(self, form):
        """Рассылка почты отложенная на 20 сек в асинхронном режиме."""
        mail_list = self.request.POST.get('mail_list', '').split('\n')
        mail_templ = self.request.POST.get('mail_templ', '')
        for s in mail_list:
            n, e = s.replace('\r', '').split('|')
            # Запускаем задачу отправку одного письма отложенную на 20 сек
            send_one_mail.apply_async((mail_templ, n, e), countdown=20)

        return super().form_valid(form)
