from django.views.generic import TemplateView

# Create your views here.
class HomePageView(TemplateView):
    template_name = 'index.html'

class WalletPageView(TemplateView):
    template_name = 'pages/index2.html'