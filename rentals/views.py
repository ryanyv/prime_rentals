from django.views import generic
from django.urls import reverse_lazy, reverse
from django.shortcuts import redirect
from django.core.mail import send_mail
from django_filters.views import FilterView
from .models import Property, TeamMember, Booking
from .forms import BookingForm, ContactForm
import django_filters


class PropertyFilter(django_filters.FilterSet):
    class Meta:
        model = Property
        fields = {
            'location': ['icontains'],
            'rental_type': ['exact'],
            'bedrooms': ['gte'],
        }


class HomeView(FilterView):
    """Render the luxury landing page as the site's homepage."""
    model = Property
    paginate_by = 10
    filterset_class = PropertyFilter
    template_name = 'luxury_home.html'


class LuxuryHomeView(FilterView): # Changed from generic.TemplateView
    model = Property
    paginate_by = 10
    filterset_class = PropertyFilter
    template_name = 'luxury_home.html'

    def get(self, request, *args, **kwargs):
        filter_fields = self.filterset_class.get_fields().keys()
        filter_params_found = False
        for param_key in request.GET.keys():
            base_param_key = param_key.split('__')[0]
            if base_param_key in filter_fields:
                filter_params_found = True
                break

        if filter_params_found and request.GET:
            query_string = request.GET.urlencode()
            return redirect(f"{reverse('rentals:property_list')}?{query_string}")

        return super().get(request, *args, **kwargs)


class LuxuryPropertiesView(generic.TemplateView):
    """Display the luxury property listings page."""
    template_name = 'luxury_properties.html'


class LuxuryAboutView(generic.TemplateView):
    """Dedicated luxury about page."""
    template_name = 'luxury_about.html'


class PropertyListView(FilterView):
    model = Property
    paginate_by = 10
    filterset_class = PropertyFilter
    template_name = 'property_list.html'


class ShortTermListView(PropertyListView):
    def get_queryset(self):
        return super().get_queryset().filter(rental_type=Property.SHORT)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Short Term Rentals'
        return context


class LongTermListView(PropertyListView):
    def get_queryset(self):
        return super().get_queryset().filter(rental_type=Property.LONG)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Long Term Rentals'
        return context


class PropertyDetailView(generic.DetailView):
    model = Property
    template_name = 'property_detail.html'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'


class TeamListView(generic.ListView):
    model = TeamMember
    template_name = 'about.html'


class ContactView(generic.FormView):
    template_name = 'contact.html'
    form_class = ContactForm
    success_url = reverse_lazy('rentals:contact')

    def form_valid(self, form):
        # Stubbed out email sending
        send_mail('Contact Inquiry', form.cleaned_data['message'], form.cleaned_data['email'], ['info@example.com'])
        return super().form_valid(form)


class BookingCreateView(generic.CreateView):
    model = Booking
    form_class = BookingForm
    template_name = 'booking_form.html'

    def form_valid(self, form):
        form.instance.property_id = self.kwargs['pk']
        response = super().form_valid(form)
        self.success_url = reverse_lazy('rentals:property_detail', kwargs={'slug': form.instance.property.slug})
        return response

