from django.contrib import admin
from .models import Stock

# Register your models here.

class StockAdmin(admin.ModelAdmin):
    list_display = ('stockName', 'stockCode', 'ipoDate', 'kospi', 'likeCount')
    search_fields = ('stockName', )

admin.site.register(Stock, StockAdmin) 