from datetime import datetime
import os
from django.conf import settings
import pandas as pd
from django.utils.timezone import make_aware
from .models import ScraperData

def int_or_none(value):
    try:
        return int(value)
    except:
        return None

def fetch_telegram_data():
    print('fetching telegram started')
    sheet_id = "194uUksIX6_qQ27RcgZ01hggRHV3ZFCcPBiF5PBn_6P4"
    # sheet_name = "Sheet1"
    tab_id = "0"
    # url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet={sheet_name}"
    url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet={tab_id}"
    data_frame = pd.read_csv(url)

    print(f"Got {len(data_frame)} Entries")

    for i in range(len(data_frame)):
        cryptocurrency = data_frame["Cryptocurrency"][i]
        ticker = data_frame["Ticker"][i]
        yesterday_total = data_frame["YESTERDAY_TOTAL"][i]
        today_total = data_frame["TODAY_TOTAL"][i]
        difference = data_frame["Difference"][i]
        yesterday_icospeaks = data_frame["yesterday_icospeaks"][i]
        today_icospeaks = data_frame["today_icospeaks"][i]
        yesterday_cryptocom = data_frame["yesterday_cryptocom"][i]
        today_cryptocom = data_frame["today_cryptocom"][i]
        yesterday_coinmarket = data_frame["yesterday_coinmarket"][i]
        today_coinmarket = data_frame["today_coinmarket"][i]
        date = data_frame["DATE"][i]

        year = date.split(' ')[0].split('-')[0]
        month = date.split(' ')[0].split('-')[1]
        day = date.split(' ')[0].split('-')[2]
        hour = date.split(' ')[1].split(':')[0]
        minute = date.split(' ')[1].split(':')[1]
        second = date.split(' ')[1].split(':')[2]

        ScraperData.objects.get_or_create(
            scraper_name = "T",
            cryptocurrency = cryptocurrency,
            ticker = ticker,
            yesterday_total = int_or_none(yesterday_total),
            today_total = int_or_none(today_total),
            difference = int_or_none(difference),
            yesterday_icospeaks = int_or_none(yesterday_icospeaks),
            today_icospeaks = int_or_none(today_icospeaks),
            yesterday_cryptocom = int_or_none(yesterday_cryptocom),
            today_cryptocom = int_or_none(today_cryptocom),
            yesterday_coinmarket = int_or_none(yesterday_coinmarket),
            today_coinmarket = int_or_none(today_coinmarket),
            date = make_aware(datetime(year=int(year), month=int(month), day=int(day), hour=int(hour), minute=int(minute), second=int(second))),
        )

    print('fetching telegram Stoped')

def fetch_reddit_data():
    print('fetching reddit started')
    sheet_id = "194uUksIX6_qQ27RcgZ01hggRHV3ZFCcPBiF5PBn_6P4"
    # sheet_name = "Sheet1"
    tab_id = "1216468972"
    # url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet={sheet_name}"
    url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet={tab_id}"
    data_frame = pd.read_csv(url)

    print(f"Got {len(data_frame)} Entries")

    for i in range(len(data_frame)):
        cryptocurrency = data_frame["Cryptocurrency"][i]
        ticker = data_frame["Ticker"][i]
        yesterday_total = data_frame["YESTERDAY_TOTAL"][i]
        today_total = data_frame["TODAY_TOTAL"][i]
        difference = data_frame["Difference"][i]
        yesterday_icospeaks = data_frame["yesterday_icospeaks"][i]
        today_icospeaks = data_frame["today_icospeaks"][i]
        yesterday_cryptocom = data_frame["yesterday_cryptocom"][i]
        today_cryptocom = data_frame["today_cryptocom"][i]
        yesterday_coinmarket = data_frame["yesterday_coinmarket"][i]
        today_coinmarket = data_frame["today_coinmarket"][i]
        date = data_frame["DATE"][i]

        year = date.split(' ')[0].split('-')[0]
        month = date.split(' ')[0].split('-')[1]
        day = date.split(' ')[0].split('-')[2]
        hour = date.split(' ')[1].split(':')[0]
        minute = date.split(' ')[1].split(':')[1]
        second = date.split(' ')[1].split(':')[2]

        ScraperData.objects.get_or_create(
            scraper_name = "R",
            cryptocurrency = cryptocurrency,
            ticker = ticker,
            yesterday_total = int_or_none(yesterday_total),
            today_total = int_or_none(today_total),
            difference = int_or_none(difference),
            yesterday_icospeaks = int_or_none(yesterday_icospeaks),
            today_icospeaks = int_or_none(today_icospeaks),
            yesterday_cryptocom = int_or_none(yesterday_cryptocom),
            today_cryptocom = int_or_none(today_cryptocom),
            yesterday_coinmarket = int_or_none(yesterday_coinmarket),
            today_coinmarket = int_or_none(today_coinmarket),
            date = make_aware(datetime(year=int(year), month=int(month), day=int(day), hour=int(hour), minute=int(minute), second=int(second))),
        )

    print('fetching reddit Stoped')
