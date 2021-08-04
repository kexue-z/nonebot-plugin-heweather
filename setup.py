import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="nonebot-plugins-heweather",
    version="0.0.1",
    author="kexue",
    author_email="xana278@qq.com",
    description="Get Heweather information and convert to pictures",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/kexue-z/nonebot-plugins-heweather",
    project_urls={
        "Bug Tracker": "https://github.com/kexue-z/nonebot-plugins-heweather/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "nonebot-plugins-heweather"},
    packages=setuptools.find_packages(where="nonebot-plugins-heweather"),
    python_requires=">=3.9",
)