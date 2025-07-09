# -*-coding: UTF-8 -*-

import sys
import subprocess


def pip_install(package, version=None, use_mirror=False, user_install=False):
    """
    使用Python代码执行pip安装
    :param package: 包名称 (str)
    :param version: 指定版本 (str, 可选)
    :param use_mirror: 启用国内镜像加速 (bool)
    :param user_install: 用户级安装（避免权限问题）(bool)
    :return: 安装结果 (bool)
    """
    # 构造安装命令
    cmd = [sys.executable, "-m", "pip", "install"]

    if user_install:
        cmd.append("--user")  # 用户级安装避免权限问题 [4](@ref)

    if version:
        full_package = f"{package}=={version}"
    else:
        full_package = package

    cmd.append(full_package)

    # 添加镜像源
    if use_mirror:
        cmd.extend(["-i", "https://pypi.tuna.tsinghua.edu.cn/simple"])  # 清华镜像源 [4](@ref)

    try:
        # 执行安装并捕获输出
        result = subprocess.run(
            cmd,
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            timeout=300  # 5分钟超时
        )
        print(f"✅ 成功安装: {full_package}")
        print("输出信息:", result.stdout[:200] + "...")  # 截取部分输出
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ 安装失败: {full_package}")
        print("错误信息:", e.stderr[:500])  # 截取关键错误
        return False
    except subprocess.TimeoutExpired:
        print("⏱️ 安装超时，请检查网络或增大超时时间")
        return False


def pip_list():
    """
    使用Python代码执行pip list命令，查看已安装的包及其版本
    :return: None
    """
    try:
        # 执行pip list命令
        result = subprocess.run(
            [sys.executable, "-m", "pip", "list"],
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        print("已安装的包及其版本：")
        print(result.stdout)
    except subprocess.CalledProcessError as e:
        print(f"❌ 查看失败")
        print("错误信息:", e.stderr)
    except Exception as e:
        print(f"运行报错: {e}")


# ===== 使用示例 =====
if __name__ == "__main__":
    pip_list()
    try:
        # 检查命令行参数
        if sys.argv[1] is not None and sys.argv[2] is None:
            # 如果只提供了一个参数（包名），则安装最新版本的包
            pip_install(sys.argv[1], use_mirror=True)
        elif sys.argv[1] is not None and sys.argv[2] is not None:
            # 如果提供了两个参数（包名和版本号），则安装指定版本的包
            pip_install(sys.argv[1], version=sys.argv[2], use_mirror=True)
        else:
            # 如果没有提供足够的参数，提示用户输入正确的参数
            print("请输入正确的参数")
            sys.exit(1)
    except Exception as e:
        # 捕获并打印运行时的任何异常
        print(f"运行报错: {e}")