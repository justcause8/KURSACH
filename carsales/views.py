from django.views.generic import TemplateView
from carsales.models import Dealer, DealerCenter, Car, Sale, Customer

class ShowCarsalesView(TemplateView):
    template_name = "carsales/show_carsales.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['dealers'] = Dealer.objects.all()
        context['dealer_centers'] = DealerCenter.objects.all()
        context['cars'] = Car.objects.all()
        context['sales'] = Sale.objects.all()
        context['customers'] = Customer.objects.all()
        return context
