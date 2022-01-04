from django.urls import path
from . import views

app_name = "fetchdata"

urlpatterns = [
    path('', views.HomeView.as_view(), name="HomeView"),
    path('scraper/<slug:slug>/', views.ScraperView.as_view(), name="ScraperView"),
    path('scraper/<slug:slug>/<int:sheet_num>/', views.SheetDataView.as_view(), name="SheetDataView"),
]
