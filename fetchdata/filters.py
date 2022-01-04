import django_filters
from django_filters import DateFilter, CharFilter, OrderingFilter
from .models import ScraperData
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, ButtonHolder, Submit

class ScraperFilter(django_filters.FilterSet):
    # start_date = DateFilter(field_name="date", lookup_expr="gte")
    # end_date = DateFilter(field_name="date", lookup_expr="lte")
    cryptocurrency = CharFilter(label="Crypto Currency", field_name="cryptocurrency", lookup_expr="icontains")
    ticker = CharFilter(label="Ticker", field_name="ticker", lookup_expr="icontains")
    order_by = OrderingFilter(field_name="order", choices = [('-yesterday_total', "yt_dec")])

    class Meta:
        model = ScraperData
        fields = '__all__'
        exclude = ['scraper_name', 'cryptocurrency', 'ticker','yesterday_total' ,'today_total' ,'difference' ,'yesterday_icospeaks' ,'today_icospeaks' ,'yesterday_cryptocom' ,'today_cryptocom' ,'yesterday_coinmarket' ,'today_coinmarket' ,'date']
