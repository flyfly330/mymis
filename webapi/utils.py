import logging
import time
import json

logger = logging.getLogger()


class ResponseHelper:

    requestNo = 1

    @staticmethod
    def create_success_response(response_data, request_ip):
        response = {'data': response_data}
        t = time.time()
        response['request_id'] = ResponseHelper.generate_request_id(request_ip, int(t))
        response['server_time'] = int(t)
        response['result_code'] = "success"
        logger.info("Create success response: " + json.dumps(response, ensure_ascii=False))

        return response

    @staticmethod
    def create_fail_response(response_data, request_ip):
        response = {'data': response_data}
        t = time.time()
        response['request_id'] = ResponseHelper.generate_request_id(request_ip, int(t))
        response['server_time'] = int(t)
        response['result_code'] = "fail"
        logger.info("Create failed response: " + json.dumps(response, ensure_ascii=False))

        return response

    @staticmethod
    def generate_request_id(request_ip, timestamp):
        request_ip = request_ip.replace('.', '')
        ResponseHelper.requestNo += 1
        request_id = "%x%s-%d" % (int(request_ip, base=16), hex(timestamp), ResponseHelper.requestNo)

        return request_id


class RequestHelper:

    @staticmethod
    def get_request_ip(request):
        if 'HTTP_X_FORWARDED_FOR' in request.META.keys():
            ip = request.META['HTTP_X_FORWARDED_FOR']
        else:
            ip = request.META['REMOTE_ADDR']

        return ip