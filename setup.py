import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="nonebot-plugin-heweather",
    version="0.1.0",
    author="kexue",
    author_email="xana278@qq.com",
    description="Get Heweather information and convert to pictures",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/kexue-z/nonebot-plugin-heweather",
    project_urls={
        "Bug Tracker": "https://github.com/kexue-z/nonebot-plugin-heweather/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    packages=['nonebot_plugin_heweather'],
    python_requires=">=3.9",
    install_requires=[
        'nonebot2',
        'Pillow',
        'httpx'
    ],
)