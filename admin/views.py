from django.views.generic import TemplateView
from django.urls import reverse_lazy
from stories.models import Story, Comment, Category, Like
from communication.models import Message, Report
from accounts.models import CustomUser
from django.db.models import Count, Q
import random
from datetime import datetime, timedelta
from collections import defaultdict

# Create your views here.
class AdminDashboardView(TemplateView):
    template_name = 'pages/index2.html'

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated or not request.user.is_staff:
            return reverse_lazy('login')  
        return super().dispatch(request, *args, **kwargs)
    
    def sales_by_week(self):
        data = []
        try:
            # Lunes de esta semana
            hoy = datetime.now().date()
            inicio_semana = hoy - timedelta(days=hoy.weekday())
            fin_semana = inicio_semana + timedelta(days=7)

            tipo_pago_totales = defaultdict(lambda: [0] * 7)
            ventas = Story.objects.filter(updated_at__range=[inicio_semana, fin_semana])

            for venta in ventas:
                dia_semana = venta.created_at.weekday()  # 0 = lunes
                if venta.is_active:
                    tipo_pago_totales["En proceso"][dia_semana] += float(1)
                
                if not venta.is_active:
                    tipo_pago_totales["Resueltas"][dia_semana] += float(1)

            data = [{'name': tipo, 'data': dias} for tipo, dias in tipo_pago_totales.items()]
            print(f"Ventas por día de la semana y tipo de pago: {data}")
            return data
        except Exception as e:
            print(f"Error al obtener ventas semanales: {e}")
            return data


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['stories'] = Story.objects.all().order_by('-created_at')[0:10]
        context['users'] = CustomUser.objects.all().order_by('-date_joined')[0:10]
        context['messages'] = Message.objects.all().order_by('timestamp')
        context['categories'] = Category.objects.all().order_by('name')
        context['reports'] = Report.objects.all().order_by('-created_at')[0:10]
        context['total_messages'] = Message.objects.count()
        context['total_users'] = CustomUser.objects.count()
        context['total_stories'] = Story.objects.count()
        context['total_comments'] = Comment.objects.count()
        context['total_likes'] = Like.objects.count()
        context['total_reports'] = Report.objects.count()
        context['cpu_traffic'] = random.randint(50, 100)  # Simulación de tráfico de CPU
        context['sales'] = self.sales_by_week()  # Agregar datos de ventas al contexto


        # Aquí puedes agregar más datos al contexto si es necesario
        return context