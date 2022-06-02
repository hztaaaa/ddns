#使用前请安装阿里云sdk
#在最下面的函数中填入AccessKey idAccessKey Secret和需要解析的域名即可
#pip3 install aliyun-python-sdk-core
#pip3 install aliyun-python-sdk-domain
#pip3 install aliyun-python-sdk-alidns
#pip3 install requests
from aliyunsdkcore.client import AcsClient #阿里云sdk必要库
from aliyunsdkcore.acs_exception.exceptions import ClientException#阿里云sdk必要库
from aliyunsdkcore.acs_exception.exceptions import ServerException#阿里云sdk必要库
from aliyunsdkalidns.request.v20150109.DescribeSubDomainRecordsRequest import DescribeSubDomainRecordsRequest#阿里云sdk获取dns解析信息库
import json
import requests
from aliyunsdkalidns.request.v20150109.UpdateDomainRecordRequest import UpdateDomainRecordRequest#阿里云sdk修改dns解析信息库

def dns(id,key,ym):#传入阿里云id（AccessKey ID） 和 key（AccessKey Secret）和ym（需要解析的域名）
       client = AcsClient(id, key, 'cn-hangzhou')#传入阿里云AccessKey ID 和 AccessKey Secret
       request = DescribeSubDomainRecordsRequest()
       request.set_accept_format('json')#默认json格式返回值
       request.set_SubDomain(ym)#需要解析域名
       response = client.do_action_with_exception(request)#/传入参数到函数取返回值json
# python2:  print(response)
       ipp=json.loads(response)
       ipp=ipp['DomainRecords']
       ipp=ipp['Record']
       ipp=ipp[0]
       idd=str(ipp['RecordId'])
       ipp=str(ipp['Value'])
       print('当前域名解析ip为：',ipp,'id为：',idd)
#/获取阿里云目前解析ip，实例化json参数取ip值
       s=requests.get('http://ip-api.com/json/?lang=zh-CN')
#引用requests库
       bip=s.json()
       bip=str(bip['query'])
#/获取本地ip，实例化json参数取ip,id值
       if ipp == bip:
            print('本地ip相同和解析ip相同')
       else:
    #/引用阿里云解析ipsdk方法，传入本地ip进行解析
            xdns = UpdateDomainRecordRequest()
            xdns.set_accept_format('json')#默认json格式返回值
            xdns.set_RecordId(idd)#传入的需要解析域名的id值
            xdns.set_RR("@")#默认主机记录为@
            xdns.set_Type("A")#默认记录类型为A
            xdns.set_Value(bip)#传入的解析域名的ip
            xxdns = client.do_action_with_exception(xdns)#/传入参数到函数后取返回值json
            print(str(xxdns, encoding='utf-8'))
            print('解析后ip为：',bip)
            print('解析成功')


if __name__ == '__main__':
    dns('填入AccessKey id','填入AccessKey Secret','填入需要解析的域名')

