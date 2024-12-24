# ARL项目

## 项目简介
ARL (Asset Reconnaissance Light) 是一个轻量级的资产侦察工具，用于帮助安全研究人员进行资产管理和风险评估。本工具提供了强大的命令行接口，支持多种资产侦察任务的创建和管理。

## 功能特点
- 任务管理系统
- 站点信息查询
- URL信息收集
- 文件泄露检测
- 批量任务处理
- JSON格式输出支持
- 多目标扫描

## 安装说明
### 环境要求
- Python 3.7+
- pip包管理器

### 依赖包
- colorama：命令行颜色支持
- argparse：命令行参数解析

### 安装步骤
1. 克隆仓库
```bash
git clone https://github.com/your-username/arl.git
cd arl
```

2. 安装依赖
```bash
pip install -r requirements.txt
```

## 使用说明
### 初始化
```yaml
#更新config目录下的config.yaml文件，配置相关参数
api:
  host: "" # ARL服务器IP
  port: 5003
  key: "" #APIkey
  policy_id: "" #策略ID
  ```
### 命令行参数
```bash
# 查看帮助信息
python arlapitools.py -h

# 列出所有任务
python arlapitools.py -l

# 查看站点信息
python arlapitools.py -s

# 查看URL信息
python arlapitools.py -u

# 查看文件泄露信息
python arlapitools.py -f

# 创建单目标任务
python arlapitools.py -n "测试任务" -t example.com

# 从文件创建批量任务
python arlapitools.py -n "批量任务" -tf targets.txt
```

### 输出控制
- `--json`: 以JSON格式输出结果
- `-q` 或 `--quiet`: 安静模式，只输出结果
- `-v` 或 `--version`: 显示版本信息

## 项目结构
```
arl/
├── arlapitools.py  # 主入口文件
├── cli.py         # 命令行接口实现
├── core/          # 核心功能模块
└── utils/         # 工具函数
```

## 配置说明
配置文件位于 `config/` 目录下，可根据需要修改相关配置。

## 贡献指南
欢迎提交Issue和Pull Request来帮助改进项目。在提交代码前，请确保：
1. 代码符合Python代码规范
2. 添加必要的注释和文档
3. 确保所有测试通过

## 许可证
本项目采用 MIT 许可证
