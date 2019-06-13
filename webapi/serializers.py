from rest_framework import serializers
from order_service.models import  Order
import re

REGEX_MOBILE = re.compile(r"1\d{10}")  # 手机号简单校验，全数字/1开头/共11位（未做号段限制）


class OrderSerializer(serializers.ModelSerializer):

    def validate_shipping_tel(self, shipping_tel):
        if not re.match(REGEX_MOBILE, shipping_tel):
            # REGEX_MOBILE表示手机的正则表达式
            raise serializers.ValidationError("手机号码格式不正确")
        return shipping_tel

    class Meta:
        model = Order
        fields = ('id', 'order_person', 'shipping_person', 'shipping_tel', 'shipping_address',
                  'amount', 'type', 'comment', 'order_date', 'create_time', 'update_time')
