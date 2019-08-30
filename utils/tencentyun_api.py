# -*- coding: utf-8 -*-
# @Time    : 2019/8/30 11:52 AM
# @Author  : Joe
# @Site    : 
# @File    : tencentyun_api.py
# @Software: PyCharm
# @function: xxxxx

import json
from tencentcloud.common import credential
from tencentcloud.common.exception.tencent_cloud_sdk_exception import TencentCloudSDKException
from tencentcloud.cvm.v20170312 import cvm_client, models


class TencentYun_api:
    def __init__(self, tencentyun_ak, tencentyun_sk):
        """
        认证对象
        :param tencentyun_ak:
        :param tencentyun_sk:
        :param region:
        """
        try:
            self.cred = credential.Credential(tencentyun_ak, tencentyun_sk)
        except TencentCloudSDKException as e:
            print(e)

    def get_describe_instances(self, region):
        """
        请求cvm实例
        :param region:
        :return:
        """
        try:
            client = cvm_client.CvmClient(self.cred, region)
            request = models.DescribeInstancesRequest()
            response = client.DescribeInstances(request)
            data_json = json.loads(response.to_json_string())
            return data_json
        except TencentCloudSDKException as e:
            return e

    def stop_instances(self):
        pass
