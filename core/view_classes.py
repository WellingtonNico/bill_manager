from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import UpdateView,CreateView,ListView


class CustomContextMixin:
    """
    deve se tomar cuidado ao usar este mixin com o mixin de permissões, pois 
    as permissões podem não funcionar
    """
    extra_form_kwargs_to_eval = {}
    extra_context_to_eval = {}
    extra_context = {}

    def get_form_kwargs(self,**kwargs):
        """
        modifica o método da classe original para enviar argumentos customizados
        para o formulário, todos os argumentos estarão dentro da chave 'custom_kwargs'
        """
        kwargs = super().get_form_kwargs(**kwargs)
        customKwargs = {}
        customKwargs['current_user'] = self.request.user
        for key,value in self.extra_form_kwargs_to_eval.items():
            try:
                customKwargs[key] = eval(value)
            except (SyntaxError,TypeError):
                customKwargs[key] = value
        kwargs['custom_kwargs'] = customKwargs
        return kwargs

    def get_context_data(self,**kwargs):
        """
        modifica o método original da classe, usando o eval em um dicinonário
        para abstrair toda a parte chata de obter o contexto e depois entregar
        """
        context = super().get_context_data(**kwargs)
        for key,value in self.extra_context_to_eval.items():
            try:
                context[key] = eval(value)
            except (SyntaxError,TypeError):
                context[key] = value
        return context


class CustomCreateView(CustomContextMixin,SuccessMessageMixin,CreateView):
    def get_success_message(self, cleaned_data):
        gender = 'o'
        try:
            gender = self.model.gender
        except AttributeError:
            pass
        return f'{self.model._meta.verbose_name} criad{gender} com sucesso!' 
    

class CustomUpdateView(CustomContextMixin,SuccessMessageMixin,UpdateView):
    def get_success_message(self, cleaned_data):
        self.model = self.get_object().__class__
        try:
            gender = self.model.gender
        except AttributeError:
            gender = 'o'
        return f'{self.model._meta.verbose_name} atualizad{gender} com sucesso!' 


class CustomListView(CustomContextMixin,ListView):
    page_size_param = 'page_size'
    page_number_param = 'page'
    page_ordering_param = 'ordering'
    default_ordering = None
    default_page_size = 40
    exclude_params = []
    list_params = []
    get_queryset_function_to_eval = ''

    def get_ordering(self):
        return self.request.GET.get(self.page_ordering_param,self.default_ordering)

    def get_paginate_by(self, queryset):
        return self.request.GET.get(self.page_size_param,self.default_page_size)

    def build_filters_dict(self) -> dict:
        filters = {}
        for key in self.request.GET.keys():
            if key != self.page_number_param and key != self.page_size_param and not key in self.exclude_params and not key == self.page_ordering_param:
                value = self.request.GET.get(key)
                if value:
                    if key in self.list_params:
                        filters[key] = value.split(',')
                    else:
                        filters[key] = value
        return filters
    
    def get_queryset(self):
        if self.get_queryset_function_to_eval:
            queryset = eval(self.get_queryset_function_to_eval)().filter(**self.build_filters_dict())
        else:
            queryset = super().get_queryset().filter(**self.build_filters_dict())
        ordering = self.get_ordering()
        if ordering:
            return queryset.order_by(ordering)
        return queryset

