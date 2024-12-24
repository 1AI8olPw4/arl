from utils.request import make_request
from utils.output import create_table, get_status_color, format_output

def query_leaks():
    """查询文件泄露信息"""
    response = make_request('GET', 'fileleak/')
    
    def table_format(data):
        table = create_table(['序号', 'Title', 'Url', 'Status_Code', 'Site'])
        if not table:
            return
            
        for i, item in enumerate(data, 1):
            status_color = get_status_color(item['status_code'])
            
            table.add_row([
                i,
                item['title'],
                item['url'],
                status_color,
                item['site']
            ])
        print(table)
    
    # 准备用于JSON输出的数据
    output_data = []
    for item in response['items']:
        output_data.append({
            'title': item['title'],
            'url': item['url'],
            'status_code': item['status_code'],
            'site': item['site']
        })
    
    format_output(output_data, table_format) 