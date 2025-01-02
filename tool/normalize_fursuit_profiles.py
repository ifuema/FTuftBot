import os
import shutil
from typing import Dict, List, Tuple


def process_profile_file(file_path: str) -> Dict[str, str]:
    """读取个人资料文件并返回解析后的数据字典"""
    data = {}
    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            if ':' in line:
                key, value = line.split(':', 1)
                data[key.strip()] = value.strip()
    return data


def save_profile(data: List[str], file_path: str) -> None:
    """将修改后的数据保存回文件"""
    with open(file_path, 'w', encoding='utf-8') as f:
        for value in data:
            f.write(f"{value}\n")


def process_all_profiles(base_dir: str, processor_func) -> List[Tuple[str, Dict[str, str]]]:
    """
    处理所有个人资料文件

    Args:
        base_dir: 包含所有page文件夹的目录
        processor_func: 处理数据的函数，接收数据字典作为参数并返回修改后的字典

    Returns:
        处理失败的文件列表
    """
    failures = []

    # 遍历所有page文件夹
    for folder_name in os.listdir(base_dir):
        if not folder_name.startswith('fursuit_page_'):
            continue

        profile_path = os.path.join(base_dir, folder_name, 'fursuit_profile.txt')
        if not os.path.exists(profile_path):
            continue

        try:
            # 创建备份
            backup_path = profile_path + '.bak'
            shutil.copy2(profile_path, backup_path)

            # 读取并处理数据
            data = process_profile_file(profile_path)
            modified_data = processor_func(data)

            # 保存修改后的数据
            save_profile(modified_data, profile_path)
            print(f"已成功处理: {profile_path}")

        except Exception as e:
            failures.append((profile_path, str(e)))
            print(f"处理失败 {profile_path}: {str(e)}")

            # 如果处理失败，从备份恢复
            if os.path.exists(backup_path):
                shutil.copy2(backup_path, profile_path)

    return failures


def processor(data: Dict[str, str]) -> List[str]:
    """示例处理函数 - 可以根据需求修改"""
    modified = [f"{data['昵称']}({data['拥有者']})"]
    modified.append(f"种族: {data['种族']}")
    modified.append(f"制作者: {data['制作者']}")
    if '其他设定' in data:
        modified.append(f"{data['其他设定']}")
    return modified


if __name__ == "__main__":
    base_directory = "../images/page"  # 存放所有page文件夹的目录
    failures = process_all_profiles(base_directory, processor)

    # 打印处理失败的文件
    if failures:
        print("\n处理失败的文件:")
        for path, error in failures:
            print(f"- {path}: {error}")
    else:
        print("\n所有文件处理成功!")