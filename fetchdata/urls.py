from django.urls import path
from . import views

app_name = "fetchdata"

urlpatterns = [
    path('', views.HomeView.as_view(), name="HomeView"),
    path('scraper/<slug:slug>/', views.ScraperView.as_view(), name="ScraperView"),
    path('scraper/<slug:slug>/<slug:scrap_opt>/', views.SheetDataView.as_view(), name="SheetDataView"),
    path('scraper_data/<slug:slug>/<slug:scrap_opt>/', views.ScraperDataView.as_view(), name="ScraperDataView"),
    path('telegram_number_add/', views.TelegramNumberView.as_view(), name="TelegramNumberView"),
    path('manage_sequence/', views.ManageSequenceView.as_view(), name="ManageSequenceView"),
]
