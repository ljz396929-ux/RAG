"""
yaml
k: v
"""
import yaml
from utils.path_tool import get_abs_path


def load_rag_config(config_file: str = get_abs_path('config/rag.yml'), encoding: str = 'utf-8'):
    with open(config_file, 'r', encoding=encoding) as f:
        return yaml.load(f, Loader=yaml.FullLoader)


def load_chroma_config(config_file: str = get_abs_path('config/chroma.yml'), encoding: str = 'utf-8'):
    with open(config_file, 'r', encoding=encoding) as f:
        return yaml.load(f, Loader=yaml.FullLoader)


def load_prompts_config(config_file: str = get_abs_path('config/prompts.yml'), encoding: str = 'utf-8'):
    with open(config_file, 'r', encoding=encoding) as f:
        return yaml.load(f, Loader=yaml.FullLoader)


def load_agent_config(config_file: str = get_abs_path('config/agent.yml'), encoding: str = 'utf-8'):
    with open(config_file, 'r', encoding=encoding) as f:
        # yaml.load 会把 YAML 转成 Python 字典：
        return yaml.load(f, Loader=yaml.FullLoader)


rag_conf = load_rag_config()
chroma_conf = load_chroma_config()
prompts_conf = load_prompts_config()
agent_conf = load_agent_config()


if __name__ == '__main__':
    print(agent_conf['chat_model_name'])
