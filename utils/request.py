import requests
import urllib3
from config.settings import settings

urllib3.disable_warnings()

def get_headers(content_type=None):
    """获取请求头"""
    headers = {
        'accept': 'application/json',
        'Token': settings.api_key
    }
    if content_type:
        headers["Content-Type"] = content_type
    return headers

def make_request(method, endpoint, **kwargs):
    """统一的请求处理"""
    url = settings.api_url + endpoint
    kwargs.setdefault('verify', False)
    kwargs.setdefault('headers', get_headers())
    
    try:
        response = requests.request(method, url, **kwargs)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        raise Exception(f"请求错误: {e}") 