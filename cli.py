import argparse
from textwrap import fill
from core import task, site, url, file
from colorama import Fore, Style

def main():
    parser = argparse.ArgumentParser(
        description=Fore.GREEN + 'ARL(Asset Reconnaissance Light) 资产侦察灯塔系统命令行工具' + Style.RESET_ALL,
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=Fore.CYAN + '''
使用示例:
    %(prog)s -l                          列出所有任务
    %(prog)s -s                          查看站点信息
    %(prog)s -u                          查看URL信息
    %(prog)s -f                          查看文件泄露信息
    
    %(prog)s -n "测试" -t example.com     创建单目标任务
    %(prog)s -n "批量" -tf targets.txt    从文件创建批量任务


''' + Style.RESET_ALL,
    )
    
    # 查询相关参数 - 使用互斥组
    query_group = parser.add_mutually_exclusive_group()
    query_group.add_argument('-l', '--list',
                           action='store_true',
                           dest='list_tasks',
                           help='列出所有任务信息')
    
    query_group.add_argument('-s', '--site',
                           action='store_true',
                           help='查询站点信息')
    
    query_group.add_argument('-f', '--file',
                           action='store_true',
                           dest='file_leak',
                           help='查询文件泄露信息')
    
    query_group.add_argument('-u', '--url',
                           action='store_true',
                           help='查询URL信息')

    # 任务创建相关参数
    task_group = parser.add_argument_group(Fore.YELLOW + '任务创建参数' + Style.RESET_ALL)
    task_group.add_argument('-n', '--name',
                           type=str,
                           help='任务名称')
    
    # 修改target参数组，使用互斥组
    target_group = task_group.add_mutually_exclusive_group()
    target_group.add_argument('-t', '--target',
                            type=str,
                            help='扫描目标 (域名或IP)')
    
    target_group.add_argument('-tf', '--target-file',
                            type=str,
                            help='从文件加载扫描目标 (每行一个目标)')

    # 输出格式控制
    output_group = parser.add_argument_group(Fore.YELLOW + '输出控制' + Style.RESET_ALL)
    output_group.add_argument('--json',
                             action='store_true',
                             help='以JSON格式输出结果')
    
    output_group.add_argument('-q', '--quiet',
                             action='store_true',
                             help='安静模式，只输出结果')
    
    # 版本信息
    parser.add_argument('-v', '--version',
                       action='version',
                       version=Fore.CYAN + '%(prog)s ' + Style.BRIGHT + '1.0.0' + Style.RESET_ALL,
                       help='显示版本信息')

    args = parser.parse_args()
    
    try:
        # 设置全局输出格式
        from utils.output import set_output_format
        set_output_format(json_format=args.json, quiet=args.quiet)
        
        # 处理查询命令
        if args.list_tasks:
            task.list_tasks()
        elif args.site:
            site.query_sites()
        elif args.file_leak:
            file.query_leaks()
        elif args.url:
            url.query_urls()
        # 处理任务创建
        elif args.name:
            if not (args.target or args.target_file):
                parser.error("创建任务时必须指定目标 (-t/--target) 或目标文件 (-tf/--target-file)")
            if args.target:
                task.create_task(args.name, args.target)
            else:
                task.create_task_from_file(args.name, args.target_file)
        else:
            parser.print_help()
    except Exception as e:
        print(f"错误: {e}")
        return 1
    
    return 0 