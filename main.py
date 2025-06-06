import datetime

import requests
import json
import os

default_appID = "wx966de8558149bf3f"
default_appSecret = "0925ef3d32bfe5e907d7e672b4e9dd88"
# 收信人ID即 用户列表中的微信号，见上文
default_openIds = ["o8_NG7F4seO45Pq2op-vwx05Prbs", "o8_NG7NEoFugvlcUWDRBdJHrBW6Q"]
# 天气预报模板ID
default_weather_template_id = 'OwG9BX_bOLetWNlwJgKXuGn6bBA0BS8Db4OzORg2laE'
# 从环境变量中获取
appID = os.environ.get("APP_ID", default_appID)
appSecret = os.environ.get("APP_SECRET", default_appSecret)
# 收信人ID即 用户列表中的微信号，
openIds_env = os.environ.get("OPEN_IDS")
if openIds_env:
    openIds = openIds_env.split(',')
else:
    openIds = default_openIds
# 天气预报模板ID
weather_template_id = os.environ.get("WEATHER_TEMPLATE_ID", default_weather_template_id)


def get_access_token():
    # 获取access token的url
    url = 'https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid={}&secret={}' \
        .format(appID.strip(), appSecret.strip())
    response = requests.get(url).json()
    print(response)
    access_token = response.get('access_token')
    return access_token


def get_caiyun_weather(longitude, latitude):
    url = f"https://api.caiyunapp.com/v2.6/OMFSneNpNxLXXUOf/{longitude},{latitude}/realtime"
    response = requests.get(url)
    weather_data = response.json()
    if weather_data['status'] == 'ok':
        realtime_data = weather_data['result']['realtime']
        temperature = realtime_data['temperature']
        humidity = realtime_data['humidity']
        skycon = realtime_data['skycon']
        wind_speed = realtime_data['wind']['speed']
        wind_direction = realtime_data['wind']['direction']
        pressure = realtime_data['pressure']
        apparent_temperature = realtime_data['apparent_temperature']
        precipitation_intensity = realtime_data['precipitation']['local']['intensity']
        air_quality_description_chn = realtime_data['air_quality']['description']['chn']

        comfort_description = realtime_data['life_index']['comfort']['desc']
        pm25 = realtime_data['air_quality']['pm25']
        aqi_chn = realtime_data['air_quality']['description']['usa']

        skycon_mapping = {
            "CLEAR_DAY": "晴（白天）",
            "CLEAR_NIGHT": "晴（夜间）",
            "PARTLY_CLOUDY_DAY": "多云（白天）",
            "PARTLY_CLOUDY_NIGHT": "多云（夜间）",
            "CLOUDY": "阴",
            "LIGHT_HAZE": "轻度雾霾",
            "MODERATE_HAZE": "中度雾霾",
            "HEAVY_HAZE": "重度雾霾",
            "LIGHT_RAIN": "小雨",
            "MODERATE_RAIN": "中雨",
            "HEAVY_RAIN": "大雨",
            "STORM_RAIN": "暴雨",
            "FOG": "雾",
            "LIGHT_SNOW": "小雪",
            "MODERATE_SNOW": "中雪",
            "HEAVY_SNOW": "大雪",
            "STORM_SNOW": "暴雪",
            "DUST": "浮尘",
            "SAND": "沙尘",
            "WIND": "大风",
        }
        skycon_description = skycon_mapping.get(skycon, skycon)

        wind_direction_mapping = {
            0: "北风",
            45: "东北风",
            90: "东风",
            135: "东南风",
            180: "南风",
            225: "西南风",
            270: "西风",
            315: "西北风"
        }

        closest_direction = min(wind_direction_mapping.keys(), key=lambda k: abs(k - wind_direction))
        wind_direction_description = wind_direction_mapping.get(closest_direction, str(wind_direction))

        precipitation_mapping = {
            0: "无降水",
            0.1: "微量降水",
            0.5: "小雨",
            2: "中雨",
            5: "大雨",
            10: "暴雨",
            20: "大暴雨",
            50: "特大暴雨"
        }
        closest_precipitation = min(precipitation_mapping.keys(), key=lambda k: abs(k - precipitation_intensity))
        precipitation_description = precipitation_mapping.get(closest_precipitation, str(precipitation_intensity))

        weather_info = {
            "temperature": temperature,
            "humidity": humidity,
            "skycon": skycon_description,
            "wind_speed": wind_speed,
            "wind_direction": wind_direction_description,
            "pressure": pressure,
            "apparent_temperature": apparent_temperature,
            "precipitation_intensity": precipitation_description,
            "air_quality_description_chn": air_quality_description_chn,
            "pm25": pm25,
            "aqi_chn": aqi_chn,
            "comfort_description": comfort_description,
        }
        return weather_info
    else:
        print("获取彩云天气信息失败")
        return None


def get_wind_force_level_numeric_kmh(wind_speed_kmh):
    """
    根据风速 (km/h) 获取风力等级 (数字等级)。

    Args:
        wind_speed_kmh: 风速，单位为千米/小时 (km/h)。

    Returns:
        风力等级，返回字符串类型的数字等级 (例如: "0级", "1级", "2级" 等)。
    """
    if wind_speed_kmh < 1:
        return "0级"
    elif wind_speed_kmh < 6:
        return "1级"
    elif wind_speed_kmh < 12:
        return "2级"
    elif wind_speed_kmh < 20:
        return "3级"
    elif wind_speed_kmh < 29:
        return "4级"
    elif wind_speed_kmh < 39:
        return "5级"
    elif wind_speed_kmh < 50:
        return "6级"
    elif wind_speed_kmh < 62:
        return "7级"
    elif wind_speed_kmh < 75:
        return "8级"
    elif wind_speed_kmh < 89:
        return "9级"
    elif wind_speed_kmh < 103:
        return "10级"
    elif wind_speed_kmh < 118:
        return "11级"
    elif wind_speed_kmh < 134:
        return "12级"
    elif wind_speed_kmh < 150:
        return "13级"
    elif wind_speed_kmh < 167:
        return "14级"
    elif wind_speed_kmh < 184:
        return "15级"
    elif wind_speed_kmh < 202:
        return "16级"
    elif wind_speed_kmh <= 220:  # 图片上最大值是 220 km/h
        return "17级"
    else:
        return "17级以上"


def send_updated_weather(access_token, weather_info):
    import datetime
    today = datetime.date.today()
    today_str = today.strftime("%Y年%m月%d日")

    url = 'https://api.weixin.qq.com/cgi-bin/message/template/send?access_token={}'.format(access_token)

    for openId in openIds:
        body = {
            "touser": openId,
            "template_id": weather_template_id,
            "url": "https://ww1xhqc-deno-weathe-55.deno.dev/",
            "data": {
                "date": {
                    "value": today_str
                },
                "region": {
                    "value": "拱墅区"
                },
                "weather_info": {
                    "value": weather_info.get('skycon', '未知')
                },
                "temperature": {
                    "value": f"{weather_info.get('temperature', '未知'):.2f}°C"
                },
                "wind_direction": {
                    "value": weather_info.get('wind_direction', '未知')
                },
                "humidity": {
                    "value": f"{float(weather_info.get('humidity', 0)) * 100:.0f}%" if weather_info.get(
                        'humidity') != '未知' and isinstance(weather_info.get('humidity'), (int, float)) else '未知'
                },
                "wind_speed": {
                    "value": get_wind_force_level_numeric_kmh(weather_info.get('wind_speed', 0))
                },
                "pressure": {
                    "value": f"{weather_info.get('pressure', '未知'):.2f}"
                },
                "apparent_temperature": {
                    "value": f"{weather_info.get('apparent_temperature', '未知'):.2f}°C"
                },
                "precipitation_intensity": {
                    "value": weather_info.get('precipitation_intensity', '未知')
                },
                "air_quality_description_chn": {
                    "value": weather_info.get('air_quality_description_chn', '未知')
                },
                "pm25": {
                    "value": weather_info.get('pm25', '未知')
                },
                "aqi_chn": {
                    "value": weather_info.get('aqi_chn', '未知')
                },
                "comfort_description": {
                    "value": weather_info.get('comfort_description', '未知')
                },
                "today_note": {
                    "value": "点击查看历史上的今天"  # 每日情话
                }
            }
        }
        print(requests.post(url, json.dumps(body)).text)


if __name__ == '__main__':
    weather = get_caiyun_weather(120.179723, 30.307765)
    send_updated_weather(get_access_token(), weather)
