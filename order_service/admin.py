import xlwt
from django.contrib import admin
from django.http import StreamingHttpResponse

from .models import Order

# Register your models here.

filename = "excel_export.xls"


class OrderAdmin(admin.ModelAdmin):
    actions = ["saveexecl"]  # 自定义的action（导出到excel表格）
    list_display = ('order_person', 'shipping_person', 'shipping_tel', 'shipping_address', 'order_date',)
    search_fields = ('order_person', 'shipping_person', 'shipping_tel', 'shipping_address',)
    list_filter = ('order_person',)
    list_per_page = 100

    def saveexecl(self, request, queryset):
        Begin = xlwt.Workbook()
        sheet = Begin.add_sheet("response")
        rows = 0
        # 写表头
        sheet.write(rows, 0, "下单人")
        sheet.write(rows, 1, "收货人")
        sheet.write(rows, 2, "收货人电话")
        rows += 1
        for query in queryset:
            # you need write colms                     # 好像有个方法可以一次性写入所有列，记不清了，只能用这种简单的方法去实现
            sheet.write(rows, 0, str(query.order_person))  # 写入第一列
            sheet.write(rows, 1, str(query.shipping_person))  # 写入第二列
            sheet.write(rows, 2, str(query.shipping_tel))  # 写入第三列
            rows += 1
        Begin.save("%s" % filename)

        def file_iterator(file_name, chuck_size=512):
            with open(file_name, "rb") as f:
                while True:
                    c = f.read(chuck_size)
                    if c:
                        yield c
                    else:
                        break

        response = StreamingHttpResponse(file_iterator(filename))
        response['Content-Type'] = 'application/octet-stream'
        response['Content-Disposition'] = 'attachment;filename="{}"'.format("result.xls")
        return response

    saveexecl.short_description = "导出Excel"  # 按钮显示名字


admin.site.register(Order, OrderAdmin)
