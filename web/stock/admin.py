from django.contrib import admin
from .models import Stock

# Register your models here.

class StockAdmin(admin.ModelAdmin):
    list_display = ('stockName', 'stockCode', 'ipoDate', 'kospi', 'likeCount')
    # <class 'stock.admin.StockAdmin'>: (admin.E126) The value of 'search_fields' must be a list or tuple.
    search_fields = ('stockName', )

admin.site.register(Stock, StockAdmin) 