from utils.request import make_request, get_headers
from utils.output import create_table, get_status_color, format_output
from colorama import Fore, Style
import time
import re
from urllib.parse import urlparse
from pathlib import Path

def clean_target(target):
    """清洗目标地址
    
    处理以下情况：
    1. 移除首尾空格和特殊字符
    2. 移除 http:// 或 https:// 前缀
    3. 移除端口号
    4. 移除路径和参数
    5. 移除 @ 等特殊字符
    
    Args:
        target: 原始目标地址
        
    Returns:
        清洗后的域名
    """
    # 移除首尾空格和特殊字符
    target = target.strip(' \t\n\r@"\'')
    
    # 尝试解析URL
    if not target.startswith(('http://', 'https://')):
        target = 'http://' + target
        
    try:
        parsed = urlparse(target)
        # 获取 netloc (域名+端口)
        domain = parsed.netloc
        
        # 移除端口号
        domain = domain.split(':')[0]
        
        # 移除用户信息（如果有）
        if '@' in domain:
            domain = domain.split('@')[1]
            
        return domain
    except Exception:
        # 如果URL解析失败，使用正则提取域名
        pattern = r'(?:[\w-]+\.)+[\w-]+' 
        match = re.search(pattern, target)
        if match:
            return match.group(0)
        return target

def process_targets_file(file_path):
    """处理目标文件
    
    Args:
        file_path: 目标文件路径
        
    Returns:
        tuple: (清洗后的目标列表, 统计信息)
    """
    try:
        file_path = Path(file_path)
        if not file_path.exists():
            raise FileNotFoundError(f"目标文件不存在: {file_path}")
            
        # 读取并处理文件
        targets = set()  # 使用集合去重
        stats = {
            'total': 0,      # 总行数
            'valid': 0,      # 有效目标数
            'invalid': 0,    # 无效行数
            'duplicate': 0,  # 重复目标数
        }
        
        with open(file_path, 'r', encoding='utf-8') as f:
            for line in f:
                stats['total'] += 1
                line = line.strip()
                if not line or line.startswith('#'):
                    stats['invalid'] += 1
                    continue
                    
                cleaned = clean_target(line)
                if cleaned:
                    if cleaned in targets:
                        stats['duplicate'] += 1
                    else:
                        targets.add(cleaned)
                        stats['valid'] += 1
                else:
                    stats['invalid'] += 1
                    
        return list(targets), stats
        
    except Exception as e:
        raise Exception(f"处理目标文件失败: {e}")

def create_task_from_file(name, file_path):
    """从文件创建任务
    
    Args:
        name: 任务名称
        file_path: 目标文件路径
    """
    # 处理目标文件
    targets, stats = process_targets_file(file_path)
    
    if not targets:
        raise Exception("没有找到有效的目标")
    
    # 显示处理统计
    print(f'\033[36m[info]\033[0m 目标文件处理统计:')
    print(f'  总行数: {stats["total"]}')
    print(f'  有效目标: {stats["valid"]}')
    print(f'  无效行数: {stats["invalid"]}')
    print(f'  重复目标: {stats["duplicate"]}')
    print('\n有效目标列表:')
    for target in targets:
        print(f'  - {target}')
    
    # 创建任务
    target_str = ','.join(targets)  # 多个目标用逗号分隔
    create_task(name, target_str)

def list_tasks():
    """列出所有任务"""
    response = make_request('GET', 'task/')
    
    def table_format(data):
        table = create_table(['任务名称', '目标地址', '当前状态', '开始时间', '结束时间', '任务ID'])
        if not table:
            return
            
        for item in data:
            status = item['status']
            if status == 'done':
                status = Fore.GREEN + status + Style.RESET_ALL
            elif status == 'stop':
                status = Fore.RED + status + Style.RESET_ALL
            else:
                status = Fore.YELLOW + status + Style.RESET_ALL
                
            table.add_row([
                item['name'],
                item['target'],
                status,
                item['start_time'],
                item['end_time'],
                item['_id']
            ])
        print(table)
    
    format_output(response['items'], table_format)

def create_task(name, target):
    """创建新任务"""
    from config.settings import settings
    
    # 清洗目标地址
    cleaned_target = clean_target(target)
    
    data = {
        "name": name,
        "task_tag": "task",
        "target": cleaned_target,  # 使用清洗后��目标
        "policy_id": settings.policy_id,
        "result_set_id": settings.policy_id
    }
    
    response = make_request('POST', 'task/policy/', 
                          json=data,
                          headers=get_headers("application/json; charset=UTF-8"))
    
    current_time = time.strftime("%H:%M:%S", time.localtime())
    if response['message'] == 'success':
        # 添加显示清洗信息
        if cleaned_target != target:
            print(f'\033[36m[info]\033[0m 目标地址已清洗: {target} -> {cleaned_target}')
        print(f'\033[36m[info]\033[0m \033[33m{current_time}\033[0m'
              f'\033[32m {response["message"]}\033[0m \033[1;31m下发任务成功！\033[0m')
    else:
        print('\033[1;32m error 下发任务失败！\033[0m') 