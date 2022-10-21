import binascii
from core.tasks import send_mail_task
from crispy_forms.helper import FormHelper
from crispy_forms.layout import HTML,Layout,Fieldset
from django import forms
from django.conf import settings
from django.contrib.auth.forms import AuthenticationForm,PasswordResetForm,SetPasswordForm,PasswordChangeForm


class SupportForm(forms.Form):
    helper = FormHelper()
    helper.layout = Layout(
        Fieldset(
            'Formulário de suporte',
            'support_reason','support_reason_explanation','support_text',
            'support_attachments','answer_to_email'
        ),
        HTML(
            ''' 
            <div class="col text-center">
                <button type="submit" class="btn btn-success"><i class="material-icons">send</i> Enviar</button>
            </div>
            '''
        )
    )
    support_reason = forms.ChoiceField(
        label='Motivo do suporte',
        choices=(
            ("Dúvida","Dúvida"),
            ("Pedir melhoria","Pedir melhoria"),
            ("Exigência","Exigência"),
            ("Sugestão de melhoria","Sugestão de melhoria"),
            ("Relatar um problema","Relatar um problema"),
            ("Outro motivo","Outro motivo"),
        ),
        # widget=forms.Select(
        #     attrs={
        #         'class':'form-control w50'
        #     }
        # )
    )
    support_reason_explanation = forms.CharField(
        label='Breve explicação do motivo',max_length=45,min_length=5,required=False,
        help_text='Caso sua opção acima for "Outro motivo", será necessário que deixe uma breve explicação',
        # widget=forms.TextInput(attrs={'class':'form-control w-100'})
    )
    support_text = forms.CharField(
        label='Escreva seu requerimento aqui',
        min_length=20,max_length=400,
        widget=forms.Textarea(
            attrs={'rows':3}
        )
    )
    support_attachments = forms.FileField(
        label='Anexos',required=False,
        help_text='Anexe imagens para um melhor esclarecimento da situação(no máximo 5 imagens até 1MB de tamanho)',
        widget=forms.FileInput(
            attrs={'multiple':True}
        )
    )
    answer_to_email = forms.EmailField(
        label='Responder para o e-mail',help_text='Insira um e-mail específico para a resposta, se acaso for necessário',
        required=False
    )

    def __init__(self,*args,**kwargs):
        customKwargs = kwargs.pop('custom_kwargs')
        self.current_user = customKwargs['current_user']
        super().__init__(*args,**kwargs)

    def clean_support_reason_explanation(self):
        value = self.cleaned_data['support_reason_explanation']
        reason = self.cleaned_data['support_reason']
        if not value and reason == 'Outro motivo':
            raise forms.ValidationError('Para este motivo é necessário deixar uma breve explicação')
        return value

    def clean_support_attachments(self):
        files = self.files.getlist('support_attachments')
        if len(files) > 5:
            raise forms.ValidationError('É possível enviar somente 5 imagens')
        for file in files:
            if not 'image/' in file.content_type:
                raise forms.ValidationError('Somente imagens são suportadas')
            if file.size > 1024000:
                raise forms.ValidationError(f'O arquivo \"{file.name}\" é maior que o tamanho permitido, que é 1MB')
        return files

    def is_valid(self) -> bool:
        if super().is_valid():
            self.send()
            return True
        else:
            return False
    
    def send(self):
        reason = self.cleaned_data['support_reason']
        support_reason_explanation = self.cleaned_data['support_reason_explanation']
        support_text = self.cleaned_data['support_text']
        attachments = {}
        for file in self.cleaned_data['support_attachments']:
            attachments[file.name] = binascii.b2a_base64(file.read()).decode('utf8')
        send_mail_task.apply_async(
            args=(
                [settings.OWNER_EMAIL_RECEIVER],
                f'Usuário {self.current_user.first_name} contatou o suporte - {support_reason_explanation if support_reason_explanation else reason}',
f'''
Email do suporte do site

usuário: {self.current_user.first_name} - {self.current_user.email}

responder para: {self.cleaned_data["answer_to_email"] if self.cleaned_data["answer_to_email"] else self.current_user.email}

motivo: {reason}

{"explicação: " if support_reason_explanation else ''}{support_reason_explanation if support_reason_explanation else ''}

texto:
{support_text}\n\n
''',            
                attachments
            )
        )


class AccessSolicitationForm(forms.Form):
    helper = FormHelper()
    helper.layout = Layout(
        Fieldset(
            'Contas Fácil',
            'name','email','phone','message'
        ),
        HTML(
            ''' 
            <div class="col text-center">
                <button type="submit" class="btn btn-success"><i class="material-icons">send</i> Enviar</button>
            </div>
            '''
        )
    )

    name = forms.CharField(max_length=255,label='Nome Completo',required=True)
    email = forms.EmailField(required=True,label='Email',max_length=255)
    phone = forms.CharField(max_length=255,label='Telefone',required=False)
    message = forms.CharField(
        label='Mensagem "opcional"',
        min_length=0,max_length=400,required=False,
        widget=forms.Textarea(
            attrs={'rows':3}
        )
    )
    def is_valid(self) -> bool:
        if super().is_valid():
            self.send()
            return True
        return False

    def send(self):
        subject = f"Solicitação de Contato - {self.cleaned_data['name']}"
        emailContent = f''' 
Solicitação de Contato

Nome: {self.cleaned_data['name']}

Email: {self.cleaned_data['email']}'''
        phone = self.cleaned_data.get('phone',None)
        if phone:
            emailContent += f'\n\nTelefone: {phone}'
        message = self.cleaned_data.get('message',None)
        if message:
            emailContent += f'\n\nMensagem: \n{message}'
        send_mail_task.apply_async(
            args=(
                [settings.OWNER_EMAIL_RECEIVER],
                subject,
                emailContent
            )
        )



class CustomAuthenticationForm(AuthenticationForm):
    helper = FormHelper()
    helper.layout =Layout(
        Fieldset(
            'Contas Fácil',
            'username','password'
        ),
        HTML(
            '''
            {% if form.errors %}
                <a class="fw-bold" style="text-decoration: none;color:#31977f;" href="{% url 'password_reset' %}">Esqueci minha senha</a>
            {% endif %}
            <div class="row mt-3 justify-content-center">
                <div class="col text-center">
                    <button type="submit" class="btn btn-success"><i class="material-icons">login</i> login</button>
                </div>
            </div>
            '''
        )
    )

class CustomPasswordResetForm(PasswordResetForm):
    helper = FormHelper()
    helper.layout =Layout(
        Fieldset(
            'Recuperação de senha',
            'email',
        ),
        HTML(
            '''
            <div class="row mt-3 justify-content-center">
                <div class="col text-center">
                    <button type="submit" class="btn btn-success"><i class="material-icons">done</i> Enviar Email</button>
                </div>
            </div>
            '''
        )
    )


class CustomSetPasswordForm(SetPasswordForm):
    helper = FormHelper()
    helper.layout =Layout(
        Fieldset(
            'Recuperação de senha',
            'new_password1','new_password2'
        ),
        HTML(
            '''
            <div class="row mt-3 justify-content-center">
                <div class="col text-center">
                    <button type="submit" class="btn btn-success"><i class="material-icons">done</i> Alterar</button>
                </div>
            </div>
            '''
        )
    )

class CustomPasswordChangeForm(PasswordChangeForm):
    helper = FormHelper()
    helper.layout =Layout(
        Fieldset(
            'Alteração de Senha',
            'old_password','new_password1','new_password2'
        ),
        HTML(
            '''
            <div class="row mt-3 justify-content-center">
                <div class="col text-center">
                    <button type="submit" class="btn btn-success"><i class="material-icons">done</i> Alterar</button>
                </div>
            </div>
            '''
        )
    )