#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
自动更新 _contributions 目录中的 GitHub 仓库统计信息（stars 和 forks）
使用 GitHub REST API 获取实时数据
"""

import requests
import re
from pathlib import Path
import time

def format_number(num):
    """
    格式化数字显示
    例如: 8300 -> "8.3k", 1900 -> "1.9k", 285 -> "285"
    """
    if num >= 1000:
        formatted = f"{num/1000:.1f}k"
        # 移除不必要的 .0
        if formatted.endswith('.0k'):
            formatted = formatted[:-3] + 'k'
        return formatted
    return str(num)

def get_repo_stats(repo_url):
    """
    从 GitHub 仓库 URL 获取 stars 和 forks 数量
    
    Args:
        repo_url: GitHub 仓库 URL (例如: https://github.com/owner/repo)
    
    Returns:
        tuple: (stars, forks) 格式化后的字符串，如果失败则返回 (None, None)
    """
    # 从 URL 中提取 owner 和 repo 名称
    match = re.search(r'github\.com/([^/]+)/([^/\.]+)', repo_url)
    if not match:
        print(f"  ⚠️  无法解析 GitHub URL: {repo_url}")
        return None, None
    
    owner, repo = match.groups()
    
    # 调用 GitHub API
    api_url = f'https://api.github.com/repos/{owner}/{repo}'
    
    try:
        response = requests.get(api_url, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            stars = data['stargazers_count']
            forks = data['forks_count']
            
            return format_number(stars), format_number(forks)
        elif response.status_code == 404:
            print(f"  ❌ 仓库不存在: {owner}/{repo}")
        elif response.status_code == 403:
            print(f"  ❌ API 请求限制（rate limit）")
            print(f"  提示: 可以设置 GITHUB_TOKEN 环境变量来增加请求限制")
        else:
            print(f"  ❌ API 请求失败 (状态码: {response.status_code})")
    
    except requests.exceptions.RequestException as e:
        print(f"  ❌ 网络请求失败: {e}")
    
    return None, None

def update_contribution_file(file_path):
    """
    更新单个 contribution 文件中的 stars 和 forks 数据
    
    Args:
        file_path: 文件路径
    
    Returns:
        bool: 是否成功更新
    """
    print(f"\n📄 处理文件: {file_path.name}")
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        print(f"  ❌ 读取文件失败: {e}")
        return False
    
    # 提取 repo URL
    repo_match = re.search(r'repo:\s*(.+)', content)
    if not repo_match:
        print(f"  ⚠️  未找到 repo URL，跳过")
        return False
    
    repo_url = repo_match.group(1).strip()
    print(f"  🔗 仓库: {repo_url}")
    
    # 获取最新的 stars 和 forks
    stars, forks = get_repo_stats(repo_url)
    
    if stars is None or forks is None:
        return False
    
    # 检查是否需要更新
    old_stars = re.search(r'stars:\s*"([^"]*)"', content)
    old_forks = re.search(r'forks:\s*"([^"]*)"', content)
    
    old_stars_val = old_stars.group(1) if old_stars else "N/A"
    old_forks_val = old_forks.group(1) if old_forks else "N/A"
    
    if old_stars_val == stars and old_forks_val == forks:
        print(f"  ℹ️  数据未变化: ⭐ {stars}, 🍴 {forks}")
        return False
    
    # 更新 stars 和 forks
    content = re.sub(r'stars:\s*"[^"]*"', f'stars: "{stars}"', content)
    content = re.sub(r'forks:\s*"[^"]*"', f'forks: "{forks}"', content)
    
    try:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"  ✅ 更新成功: ⭐ {old_stars_val} → {stars}, 🍴 {old_forks_val} → {forks}")
        return True
    except Exception as e:
        print(f"  ❌ 写入文件失败: {e}")
        return False

def main():
    """主函数：更新所有 contribution 文件"""
    print("=" * 60)
    print("🚀 开始更新 GitHub 仓库统计信息")
    print("=" * 60)
    
    contributions_dir = Path(__file__).parent / '_contributions'
    
    if not contributions_dir.exists():
        print(f"❌ 目录不存在: {contributions_dir}")
        return
    
    # 获取所有 markdown 文件
    md_files = list(contributions_dir.glob('*.md'))
    
    if not md_files:
        print(f"⚠️  未找到任何 .md 文件")
        return
    
    print(f"📁 找到 {len(md_files)} 个文件\n")
    
    updated_count = 0
    failed_count = 0
    
    # 处理每个文件
    for file_path in sorted(md_files):
        result = update_contribution_file(file_path)
        if result:
            updated_count += 1
        else:
            failed_count += 1
        
        # 避免 API 请求过快
        time.sleep(1)
    
    # 输出总结
    print("\n" + "=" * 60)
    print("📊 更新完成！")
    print("=" * 60)
    print(f"✅ 成功更新: {updated_count} 个文件")
    print(f"⚠️  跳过/失败: {failed_count} 个文件")
    print(f"📝 总计处理: {len(md_files)} 个文件")
    print("=" * 60)

if __name__ == '__main__':
    main()

