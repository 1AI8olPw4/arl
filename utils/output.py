import json
from prettytable import PrettyTable
from colorama import Fore, Style

# 全局输出控制
_output_format = {
    'json': False,
    'quiet': False
}

def set_output_format(json_format=False, quiet=False):
    """设置输出格式"""
    _output_format['json'] = json_format
    _output_format['quiet'] = quiet

def format_output(data, table_format):
    """格式化输出
    Args:
        data: 原始数据
        table_format: 表格格式化函数
    """
    if _output_format['json']:
        # JSON格式输出
        print(json.dumps(data, ensure_ascii=False, indent=2))
    elif _output_format['quiet']:
        # 安静模式，只输出关键信息
        for item in data:
            print(f"{item.get('site', '')} {item.get('status', '')}")
    else:
        # 默认表格输出
        table_format(data)

def get_status_color(status_code):
    """获取状态码颜色"""
    if _output_format['json'] or _output_format['quiet']:
        return str(status_code)
        
    if status_code == 200:
        return Fore.GREEN + str(status_code) + Style.RESET_ALL
    elif status_code in [301, 302]:
        return Fore.YELLOW + str(status_code) + Style.RESET_ALL
    return Fore.WHITE + str(status_code) + Style.RESET_ALL

def create_table(headers, align_center=True):
    """创建统一风格的表格"""
    if _output_format['json'] or _output_format['quiet']:
        return None
        
    table = PrettyTable(headers)
    if align_center:
        table.align = 'c'
    table.hrules = 1
    table.junction_char = '+'
    table.horizontal_char = '-'
    table.vertical_char = '|'
    return table 