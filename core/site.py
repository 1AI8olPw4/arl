from utils.request import make_request
from utils.output import create_table, get_status_color, format_output
from textwrap import fill

def query_sites():
    """查询站点信息"""
    response = make_request('GET', 'site/')
    
    # 重新组织数据结构
    site_data = {}
    count = 0
    
    for item in response['items']:
        site_url = item['site']
        if site_url not in site_data:
            count += 1
            site_data[site_url] = {
                'count': count,
                'title': item['title'],
                'status': item['status'],
                'fingers': [j['name'] for j in item['finger']]
            }
        else:
            site_data[site_url]['fingers'].extend(j['name'] for j in item['finger'])
            site_data[site_url]['fingers'] = list(set(site_data[site_url]['fingers']))

    def table_format(data):
        table = create_table(['序号', '站点', '标题', '指纹', '状态码'])
        if not table:
            return
            
        # 设置每列的最大宽度
        max_widths = {
            '站点': 25,
            '标题': 15,
            '指纹': 35
        }
        
        # 设置表格样式
        table.align['指纹'] = 'l'  # 指纹列左对齐
        
        # 添加数据到表格
        for site_url, info in data.items():
            status_color = get_status_color(info['status'])
            
            # 处理指纹显示，每3个指纹换一行
            fingers = info['fingers']
            finger_groups = [fingers[i:i+3] for i in range(0, len(fingers), 3)]
            formatted_fingers = '\n'.join([', '.join(group) for group in finger_groups])
            
            # 格式化站点URL和标题
            formatted_site = fill(site_url, width=max_widths['站点'])
            formatted_title = fill(info['title'], width=max_widths['标题'])
            
            table.add_row([
                info['count'],
                formatted_site,
                formatted_title,
                formatted_fingers,
                status_color
            ])
        print(table)
    
    # 准备用于JSON输出的数据
    output_data = []
    for site_url, info in site_data.items():
        output_data.append({
            'site': site_url,
            'title': info['title'],
            'status': info['status'],
            'fingers': info['fingers']
        })
    
    format_output(output_data, lambda x: table_format(site_data)) 