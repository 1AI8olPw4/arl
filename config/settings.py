import os
import yaml
from pathlib import Path

class Settings:
    def __init__(self):
        self.config_path = self._get_config_path()
        self.config = self._load_config()
        
    def _get_config_path(self):
        """获取配置文件路径"""
        # 首先检查环境变量
        if os.getenv('ARL_CONFIG'):
            return Path(os.getenv('ARL_CONFIG'))
            
        # 然后检查项目配置目录
        project_config = Path(__file__).parent / 'config.yaml'
        if project_config.exists():
            return project_config
            
        raise Exception("找不到配置文件")
        
    def _load_config(self):
        """加载配置文件"""
        try:
            with open(self.config_path) as f:
                return yaml.safe_load(f)
        except Exception as e:
            raise Exception(f"无法加载配置文件 {self.config_path}: {e}")
            
    @property
    def api_url(self):
        """构建完整的API URL"""
        return f"https://{self.config['api']['host']}:{self.config['api']['port']}/api/"
    
    @property
    def api_key(self):
        return self.config['api']['key']
    
    @property
    def policy_id(self):
        return self.config['api']['policy_id']

# 创建全局配置实例
settings = Settings() 