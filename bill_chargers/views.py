from bill_chargers.forms import BillChargerModelForm
from bill_chargers.models import BillCharger
from core.view_classes import CustomCreateView, CustomListView, CustomUpdateView


class BillChargerListView(CustomListView):
    extra_context = {
        'PAGE_SIZES':[5,10,20,30,40,50]
    }

    def get_queryset(self):
        return self.request.user.get_billchargers().filter(**self.build_filters_dict())


class BillChargerCreateView(CustomCreateView):
    model = BillCharger
    form_class = BillChargerModelForm


class BillChargerUpdateView(CustomUpdateView):
    form_class = BillChargerModelForm

    def get_queryset(self):
        return self.request.user.get_billchargers()
    
