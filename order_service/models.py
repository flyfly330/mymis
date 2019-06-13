from django.db import models
import django.utils.timezone as timezone

# Create your models here.


class Order(models.Model):
    order_person = models.CharField(max_length=128, verbose_name='下单人')
    shipping_person = models.CharField(max_length=128, verbose_name='收货人')
    shipping_tel = models.CharField(max_length=128, verbose_name='收货人电话')
    shipping_address = models.CharField(max_length=128, verbose_name='收货地址')
    order_date = models.DateField(default=timezone.now, verbose_name='下单日期')
    amount = models.IntegerField(default=0, verbose_name='数量')
    type = models.CharField(max_length=128, verbose_name='产品类型')
    comment = models.CharField(max_length=128, verbose_name='备注')
    update_time = models.DateTimeField(auto_now=True, blank=True, null=True, verbose_name='更新时间')
    create_time = models.DateTimeField(default=timezone.now, blank=True, null=True, verbose_name='添加时间')

    def __str__(self):
        return self.order_person + "-" + self.shipping_person + self.shipping_tel

    class Meta:
        db_table = 'order'


