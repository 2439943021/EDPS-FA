from setuptools import setup, find_packages


setup(
    name='Autovalseeker',  # 项目名
    version='0.1',  # 项目版本号
    description='A brief description of your project',  # 项目简介
    packages=find_packages(),  # 自动找到项目下的所有Python包
    install_requires=[  # 项目的依赖包
        'numpy>=1.21.6',
        'pymysql>=1.0.2',
        'pyahocorasick>=1.4.2',
        'bs4',
        'jinja2'
    ],
    dependency_links=[
        'https://pypi.tuna.tsinghua.edu.cn/simple/',  # 镜像网站的地址
    ],
    entry_points={  # 定义你的项目的可执行命令
        'console_scripts': [
                'annotate = src.core.annotate.main:main',  # 命令名，入口函数
        ],
    },
)
