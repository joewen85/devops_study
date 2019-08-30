# -*- coding: utf-8 -*-
# @Time    : 2019-08-23 15:36
# @Author  : Joe
# @Site    : 
# @File    : aliyun_api.py
# @Software: PyCharm
# @function: xxxxx
import json

from aliyunsdkcore.client import AcsClient
from aliyunsdkcore.acs_exception.exceptions import ClientException
from aliyunsdkcore.acs_exception.exceptions import ServerException
from aliyunsdkecs.request.v20140526 import DescribeInstancesRequest
from aliyunsdkecs.request.v20140526 import StopInstanceRequest
from aliyunsdkecs.request.v20140526 import CreateInstanceRequest
from aliyunsdkecs.request.v20140526.DescribeBandwidthLimitationRequest import DescribeBandwidthLimitationRequest


class AliyunApi:
    """
    aliyun operation
    """
    def __init__(self, ak, sk, region):
        self.client = AcsClient(ak, sk, region)

    def get_describe_instances(self):
        # 创建request，并设置参数
        request = DescribeInstancesRequest.DescribeInstancesRequest()

        # 使用https请求
        request.set_protocol_type("https")
        request.set_PageSize(10)
        request.set_accept_format('json')

        # 发起API请求并显示返回值
        try:
            # resonse是比特流
            response = self.client.do_action_with_exception(request)
            result = str(response, encoding='utf-8')
            data_json = json.loads(result)
            return data_json
            # 服务端错误信息打印
        except ServerException as e:
            return e
            # sdk端错误信息打印
        except ClientException as e:
            return e

    def create_instances(self, image, instance_name, security_group_id, instance_type):
        request = CreateInstanceRequest.CreateInstanceRequest()
        request.set_ImageId(image)
        request.set_InstanceName(instance_name)
        request.set_SecurityGroupId(security_group_id)
        request.set_InstanceType(instance_type)
        # request.set_ClientToken()
        request.set_protocol_type("https")
        request.set_accept_format('json')

        # 发起API请求并显示返回值
        try:
            response = self.client.do_action_with_exception(request)
            print(str(response, encoding='utf-8'))
            # 服务端错误信息打印
        except ServerException as e:
            print(e)
            # sdk端错误信息打印
        except ClientException as e:
            print(e)

    def stop_instance(self, instance_id):
        """
        关闭实例
        :param instance_id:
        :return: JobId
        """
        request = StopInstanceRequest.StopInstanceRequest()
        request.set_protocol_type("https")
        request.set_accept_format('json')
        request.set_InstanceId(instance_id)

        try:
            response = self.client.do_action_with_exception(request)
            result = str(response, encoding='utf-8')
        except ServerException as e:
            result = e
        except ClientException as e:
            result = e
        return result
