from django.contrib.auth import authenticate, login
from django.http.response import Http404, HttpResponse
from django.shortcuts import redirect, render
from django.views.generic import TemplateView
from django.views import View
from .filters import ScraperFilter
from django.core.paginator import Paginator
from django.contrib.auth.forms import AuthenticationForm


from fetchdata.models import ScraperData

# Create your views here.

class HomeView(TemplateView):
    template_name = "core/index.html"

class ScraperView(View):
    def get(self, request, slug):
        print(slug)
        # data = ScraperData.objects.all()
        # filter_form = ScraperFilter(self.request.GET, queryset = data)
        # print(filter_form.qs.count())
        # kwargs['data'] = filter_form.qs
        # kwargs['filter_form'] = filter_form
        context = {'scraper_name': slug}
        return render(request, "core/scraper_detail.html", context)


class ScraperDataView(View):
    def get(self, request, slug, scrap_opt):
        print(request.user)
        print(request.user.is_authenticated)
        if not request.user.is_authenticated:
            return redirect("fetchdata:SheetDataView")

        scraper_name = [scraper_name[0] for scraper_name in ScraperData.SCRAPER_NAMES if scraper_name[1] == slug]
        if not scraper_name:
            raise Http404()
        queryset = ScraperData.objects.filter(scraper_name=scraper_name[0])

        crypto_currency = request.GET.get('crypto_currency', None)
        ticker = request.GET.get('ticker', None)

        if crypto_currency:
            queryset = queryset.filter(cryptocurrency__icontains=crypto_currency)
        if ticker:
            queryset = queryset.filter(ticker__icontains=ticker)

        paginator = Paginator(queryset, 25)
        page_number = request.GET.get('page')
        data = paginator.get_page(page_number)
        context = {"data": data}
        return render(request, "core/tebular_data.html", context)


class SheetDataView(View):
    def get(self, request, slug, scrap_opt):
        print(slug)
        print(scrap_opt)
        form = AuthenticationForm()
        context = {"form": form}
        return render(request, "core/tebular_data_login.html", context)

    def post(self, request, slug, scrap_opt):
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            context = {"slug": slug, "scrap_opt": scrap_opt}

            if scrap_opt == "msg_scrap":
                return render(request, "core/msg_scrap_settings.html", context)
            elif scrap_opt == "msg_send":
                pass
            elif scrap_opt == "auto_notify":
                pass
            elif scrap_opt == "airdrop":
                pass
            elif scrap_opt == "mem_scrap":
                pass
            elif scrap_opt == "ques_ans":
                return render(request, "core/ques_ans_settings.html", context)
            elif scrap_opt == "add_remove":
                pass
            elif scrap_opt == "custom_bot":
                pass

            raise Http404()

            # scraper_name = [scraper_name[0] for scraper_name in ScraperData.SCRAPER_NAMES if scraper_name[1] == slug]
            # if not scraper_name:
            #     raise Http404()
            # queryset = ScraperData.objects.filter(scraper_name=scraper_name[0])

            # crypto_currency = request.GET.get('crypto_currency', None)
            # ticker = request.GET.get('ticker', None)

            # if crypto_currency:
            #     queryset = queryset.filter(cryptocurrency__icontains=crypto_currency)
            # if ticker:
            #     queryset = queryset.filter(ticker__icontains=ticker)

            # paginator = Paginator(queryset, 25)
            # page_number = request.GET.get('page')
            # data = paginator.get_page(page_number)
            # context = {"data": data}
            # return render(request, "core/tebular_data.html", context)

        context = {"form": form}
        return render(request, "core/tebular_data_login.html", context)
        # scraper_name = [scraper_name[0] for scraper_name in ScraperData.SCRAPER_NAMES if scraper_name[1] == slug]
        # if not scraper_name:
        #     raise Http404()
        # queryset = ScraperData.objects.filter(scraper_name=scraper_name[0])

        # crypto_currency = request.GET.get('crypto_currency', None)
        # ticker = request.GET.get('ticker', None)

        # if crypto_currency:
        #     queryset = queryset.filter(cryptocurrency__icontains=crypto_currency)
        # if ticker:
        #     queryset = queryset.filter(ticker__icontains=ticker)

        # paginator = Paginator(queryset, 25)
        # page_number = request.GET.get('page')
        # data = paginator.get_page(page_number)
        # context = {"data": data}
        # return render(request, "core/tebular_data.html", context)

