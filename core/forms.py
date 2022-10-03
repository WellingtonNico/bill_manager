from django import forms
from django.utils.safestring import mark_safe

class FieldSet:
    def __init__(self,name,attributeName,fields):
        ''' 
        recebe um nome para usar no título, o atributo, e uma lista de objetos
        do tipo BoundField, que poderão ser renderizados
        '''
        self.name = name
        self.attributeName = attributeName
        self.fields = fields
    
    def __bool__(self):
        return len(self.fields) != 0

    def getFieldsHtml(self):
        content = ''
        for field in self.fields:
            errorsList = ''
            if field.errors:
                errors = ''
                for error in field.errors:
                    errors += f'<li>{error}</li>'
                errorsList = f'<ul class="errorlist">{errors}</ul>'
            content += f'<p>{errorsList}{field.label_tag()}{field.as_widget()}<span class="helptext">{field.help_text}</span></p>'
        return content

    def as_p(self):
        return mark_safe(self.getFieldsHtml())

    def as_p_with_title(self):
        return mark_safe(f'<h2 class="fieldset-title">{self.name}</h2>{self.getFieldsHtml()}')


class CustomModelForm(forms.ModelForm):
    _cleaned_custom_fields_attributes = {}
    custom_field_attributes = ()
    must_have_attributes = ()
    fieldsets = ()

    def __init__(self,custom_kwargs={},*args,**kwargs):
        '''
        todos os argumentos passados no custom_kwargs, serão setados como 
        atributos do formulário para depois serem usados nas validações por exemplo
        '''
        for key,value in custom_kwargs.items():
            setattr(self,key,value)
        super().__init__(*args,**kwargs)
        self.mountCustomAttributesDict()
        self.validateMustHaveAttributes()
        self.buildFieldSets()
        for key,field in self.fields.items():
            if key in self._cleaned_custom_fields_attributes.keys():
                field.widget.attrs.update(
                    self._cleaned_custom_fields_attributes[key]
                )

    def mountCustomAttributesDict(self):
        """ 
        adiciona os atributos customizados dinamicamente ao formulário que forem
        colocados na variável custom_field_attributes no formato de lista contendo
        túpulas no formato seguinte:
        (
            dicionário de atributos ex: {'class': 'form-control'},
            lista/túpula de fields no formato string ex: ('name','email','password')
        )
        """
        alreadyAddedFields = []
        for fieldAttribue in self.custom_field_attributes:
            if not type(fieldAttribue[0]) == dict:
                raise Exception('Valor inválido, os atributos devem ser informados em um dicionário.')
            if not type(fieldAttribue[1]) in (list,tuple):
                raise Exception('Valor inválido, os campos devem ser informados em um iterável.')
            for field in fieldAttribue[1]:
                if not field in alreadyAddedFields:
                    alreadyAddedFields.append(field)
                else:
                    raise Exception(f'O field {field} foi referenciado mais de uma vez.')
                self._cleaned_custom_fields_attributes[field] = fieldAttribue[0]

    def validateMustHaveAttributes(self):
        """
        valida a existência de atributos necessários para o funcionamento do 
        formulário, que são definidos em uma lista/túpula na variável
        must_have_attributes
        """
        if not type(self.must_have_attributes) in (list,tuple):
            raise Exception('A variável must_have_attributes, deve ser declarada como um iterável.')
        for attribute in self.must_have_attributes:
            if not hasattr(self,attribute):
                raise Exception(f'Formulário comprometido por falta de atributo requerido: {attribute}, insira o mesmo no parametro custom_kwargs:dict do formulário')
        if not hasattr(self,'current_user'):
            raise Exception('O atributo que define o usuário logado está faltando, insira a chave <current_user> no custom_kwargs do formulário.')
    
    def buildFieldSets(self):
        """
        constrói grupos de campos que podem ser chamados individualmente na interface
        os grupos precisam ser declarados em túpulas no formato seguinte:
        (<nome legível>,<nome do atributo de acesso>,<lista com os nomes dos campos>).
        após a função rodar, a classe passará a ter atributos novos com o sufixo
        "<nome do atributo de acesso>_fieldset" (ex: client_fieldset) precedidos pelos nomes de atributos dados nas túpulas
        """
        try:
            for name,attributeName,fields in self.fieldsets:
                setattr(
                    self,
                    f'{attributeName}_fieldset',
                    FieldSet(
                        name,attributeName,
                        [self[field] for field in fields if field in self.fields.keys()]
                    )
                )
        except ValueError:
            raise Exception('houve um erro ao obter os dados dos fieldsets, certifique-se de que os iteráveis foram declados no formato correto.')


################################################################################
############################# atributos mais usados ############################
################################################################################
DEFAULT_FORM_CONTROL = {
    'class':'form-control',
}

DEFAULT_SELECT2 = {
    'class':'form-control',
    'style':'max-width: 100% !important;min-width: 100% !important;',
    'placeholder':'Selecione um produto'
}

FORM_CONTROL_REQUIRED = {
    'class':'form-control',
    'required':''
}
FORM_CONTROL_REQUIRED_W30 = {
    'class':'form-control w-30',
    'required':''
}

FORM_CONTROL_W30 = {
    'class':'form-control w-30',
}

FORM_CONTROL_W50 = {
    'class':'form-control w-50',
}

FORM_CONTROL_W100 = {
    'class':'form-control w-100',
}

FORM_CONTROL_EMAIL = {
    'class':'form-control',
    'required':'',
    'autocomplete':'false'
}

DEFAULT_CHECK_BOX = {
    'class':'form-check-input',
    'type':'checkbox'
}

FORM_CONTROL_PASSWORD = {
    'class':'form-control',
    'autocomplete':'false'
}

FORM_CONTROL_READONLY = {
    'class':'form-control ',
    'readonly':'true',
}

FORM_CONTROL_READONLY_3ROW = {
    'class':'form-control ',
    'readonly':'true',
    'rows':3
}

FORM_CONTROL_READONLY_W30 = {
    'class':'form-control w-30',
    'readonly':'readonly',
}

FORM_CONTROL_3ROW = {
    'class':'form-control',
    'rows':3
}

FORM_CONTROL_15ROW = {
    'class':'form-control',
    'rows':15
}

FORM_DATE_W30 = {
    'class':'form-control w-30',
    'type':'date'
}