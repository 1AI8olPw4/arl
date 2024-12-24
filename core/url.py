from utils.request import make_request
from utils.output import create_table, get_status_color, format_output
from textwrap import fill

def query_urls():
    """查询URL信息"""
    response = make_request('GET', 'url/')
    
    def table_format(data):
        table = create_table(['序号', '标题', 'URL', '状态码'])
        if not table:
            return
            
        for i, item in enumerate(data, 1):
            status_color = get_status_color(item['status_code'])
            table.add_row([
                i,
                fill(item['title'], width=50),
                fill(item['site'], width=50),
                status_color
            ])
        print(table)
    
    format_output(response['items'], table_format) 