from rest_framework.views import APIView
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from django.http import JsonResponse

from webapi.utils import ResponseHelper, RequestHelper

from order_service.models import Order
from webapi.serializers import OrderSerializer
from rest_framework import serializers
from rest_framework.pagination import LimitOffsetPagination

from auth_service.login import Login

# Create your views here.


class GetMessageView(APIView):
    """
    Hello world method
    """

    def get(self, request):
        # 获取参数数据
        get = request.GET
        # 获取参数 a
        a = get.get('a')
        print(a)
        # 返回信息
        d = {
            'status': 1,
            'message': 'success',
            'requestPara': a
            }
        return JsonResponse(d)


class MyLimitOffsetPagination(LimitOffsetPagination):
    """
    分页基础参数配置
    """
    # 默认显示的个数
    default_limit = 10
    # 当前的位置
    offset_query_param = "offset"
    # 通过limit改变默认显示的个数
    limit_query_param = "limit"
    # 一页最多显示的个数
    max_limit = 100


class OrderPagerSerialize(serializers.ModelSerializer):
    """
    分页数据序列化
    """

    # mm=serializers.CharField(source="ug.title") #让外键列显示名称
    class Meta:
        model = Order
        fields = "__all__"
        # depth=2 #让外键列显示名称


class OrderViewSet(viewsets.GenericViewSet):

    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    @action(detail=False, methods=['get'], url_path='list')
    def query_order_list(self, request):
        """
        查询订单列表，支持多条件联合查询（与逻辑）
        :param request:
        :return:
        """
        try:
            get = request.GET
            order_person = get.get('order_person', '')
            shipping_person = get.get('shipping_person', '')
            shipping_tel = get.get('shipping_tel', '')
            results = self.queryset.filter(order_person__contains=order_person, shipping_person__contains=shipping_person,
                                           shipping_tel__contains=shipping_tel)

            # 创建分页对象
            pg = MyLimitOffsetPagination()
            # 获取分页的数据
            page_records = pg.paginate_queryset(queryset=results, request=request, view=self)
            # 对数据进行序列化
            ser = OrderPagerSerialize(instance=page_records, many=True)
            pg_response = pg.get_paginated_response(ser.data)
            response = ResponseHelper.create_success_response(pg_response.data, RequestHelper.get_request_ip(request))
        except Exception as e:
            error_msg = {"error_msg": str(e)}
            response = ResponseHelper.create_fail_response(error_msg, RequestHelper.get_request_ip(request))

        return Response(response)

    @action(detail=True, methods=['get'], url_path='detail')
    def query_order_detail(self, request, pk=None):
        """
        查询订单详情
        :param request:
        :param pk:
        :return:
        """

        try:
            order = self.queryset.filter(id=pk).first()
            if not order:
                raise Exception("订单id不存在！")
            data = {
                'id': pk,
                'order_person': {
                    'name': order.order_person
                },
                'shipping_info': {
                    'person': {
                        'name': order.shipping_person,
                        'tel': order.shipping_tel
                    },
                    'address': order.shipping_address
                },
                'type': order.type,
                'amount': order.amount,
                'comment': order.comment
            }
            response = ResponseHelper.create_success_response(data, RequestHelper.get_request_ip(request))
        except Exception as e:
            error_msg = {
                "error_msg": str(e),
            }
            response = ResponseHelper.create_fail_response(error_msg, RequestHelper.get_request_ip(request))

        return Response(response)

    @action(detail=False, methods=['post'], url_path='create')
    def create_order(self, request):
        """
        创建订单
        :param request:
        :return:
        """
        try:
            request_data = request.data
            serializer = OrderSerializer(data=request_data)  # 根据请求入参初始化序列化对象
            if serializer.is_valid():
                serializer.save()
                response = ResponseHelper.create_success_response(serializer.data, RequestHelper.get_request_ip(request))
            else:
                response = ResponseHelper.create_fail_response(serializer.errors, RequestHelper.get_request_ip(request))

        except Exception as e:
            error_msg = {
                "error_msg": str(e),
            }
            response = ResponseHelper.create_fail_response(error_msg, RequestHelper.get_request_ip(request))

        return Response(response)

    @action(detail=True, methods=['post'], url_path='update')
    def update_order(self, request, pk=None):
        try:
            request_data = request.data
            order = Order.objects.get(pk=pk)
            serializer = OrderSerializer(instance=order, data=request_data)  # 根据请求入参初始化序列化对象
            if serializer.is_valid():
                serializer.save()
                response = ResponseHelper.create_success_response(serializer.data, RequestHelper.get_request_ip(request))
            else:
                response = ResponseHelper.create_fail_response(serializer.errors, RequestHelper.get_request_ip(request))

        except Exception as e:
            error_msg = {
                "error_msg": str(e),
            }
            response = ResponseHelper.create_fail_response(error_msg, RequestHelper.get_request_ip(request))

        return Response(response)


class AuthViewSet(viewsets.GenericViewSet):

    @action(detail=False, methods=['post'], url_path='login')
    def handle_login(self, request):
        try:
            request_data = request.data
            user_name = request_data.get('user_name')
            password = request_data.get('password')
            result = Login.handle_login(request, user_name, password)
            response = ResponseHelper.create_success_response(result,
                                                              RequestHelper.get_request_ip(request))
        except Exception as e:
            error_msg = {
                "error_msg": str(e),
            }
            response = ResponseHelper.create_fail_response(error_msg, RequestHelper.get_request_ip(request))

        return Response(response)

    @action(detail=False, methods=['post'], url_path='logout')
    def handle_logout(self, request):
        try:
            result = Login.handle_logout(request)
            response = ResponseHelper.create_success_response(result,RequestHelper.get_request_ip(request))
        except Exception as e:
            error_msg = {
                "error_msg": str(e),
            }
            response = ResponseHelper.create_fail_response(error_msg, RequestHelper.get_request_ip(request))

        return Response(response)









