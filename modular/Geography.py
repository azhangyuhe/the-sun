# 作者：博客园_杠上花
# 邮箱: a2578629964@163.com
# 时间：2022年1月20日
# 编码：utf-8
# 版本：python3.8
import re
import geoip2.database

from core.Global import LOGGER

reader = geoip2.database.Reader('data/GeoLite2-City.mmdb')

'''
[*] Target: 39.99.228.188 GeoLite2-Located 
  [+] 国家编码:        CN
  [+] 国家名称:        China
  [+] 国家中文名称:    中国
  [+] 省份或州名称:    Zhejiang
  [+] 省份或州编码:    ZJ
  [+] 城市名称 :       Hangzhou
  [+] 城市邮编 :       None
  [+] 纬度:            30.294
  [+] 经度 :           120.1619
===============End======================
'''


# 查询IP地址对应的物理地址
def ip_get_location(ip_address):
    # 载入指定IP相关数据
    response = reader.city(ip_address)

    # 读取国家代码
    Country_IsoCode = response.country.iso_code
    # 读取国家名称
    Country_Name = response.country.name
    # 读取国家名称(中文显示)
    Country_NameCN = response.country.names['zh-CN']
    # 读取州(国外)/省(国内)名称
    Country_SpecificName = response.subdivisions.most_specific.name
    # 读取州(国外)/省(国内)代码
    Country_SpecificIsoCode = response.subdivisions.most_specific.iso_code
    # 读取城市名称
    City_Name = response.city.name
    # 读取邮政编码
    City_PostalCode = response.postal.code
    # 获取纬度
    Location_Latitude = response.location.latitude
    # 获取经度
    Location_Longitude = response.location.longitude

    if Country_IsoCode is None:
        Country_IsoCode = "None"
    if Country_Name is None:
        Country_Name = "None"
    if Country_NameCN is None:
        Country_NameCN = "None"
    if Country_SpecificName is None:
        Country_SpecificName = "None"
    if Country_SpecificIsoCode is None:
        Country_SpecificIsoCode = "None"
    if City_Name is None:
        City_Name = "None"
    if City_PostalCode is None:
        City_PostalCode = "None"
    if Location_Latitude is None:
        Location_Latitude = "None"
    if Location_Longitude is None:
        Location_Longitude = "None"

    return Country_IsoCode, Country_Name, Country_NameCN, Country_SpecificName, Country_SpecificIsoCode, City_Name, City_PostalCode, str(
        Location_Latitude), str(Location_Longitude)


# 检验和处理ip地址
def scan(scanner):
    LOGGER.info(f'[*] {scanner.ipv4}_Geography')
    ip_match = r"^(?:(?:25[0-5]|2[0-4][0-9]|1[0-9][0-9]|0?[0-9]?[1-9]|0?[1-9]0)\.)(?:(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){2}(?:25[0-4]|2[0-4][0-9]|1[0-9][0-9]|0?[0-9]?[1-9]|0?[1-9]0)$"
    if re.match(ip_match, scanner.ipv4):
        try:
            scanner.ip_location.extend(list(ip_get_location(scanner.ipv4)))
        except Exception as error:
            print(f'Geography_{error}')
    else:
        print(scanner.ipv4)
