# nonebot-plugin-heweather

获取和风天气信息并转换为图片

# 和风天气API图标信息编号变化

由于和风天气图标ID和图标发生变化
* 在2021.11.30前创建的API将保持原有信息
* 之后创建的API将使用新版图标信息
* 旧版API使用`pip install nonebot-plugin-heweather==0.2.1`进行安装
* 新版API图标已更新，可直接安装
* 图标适配还没做，打算重写，先等等吧～

# 安装

直接使用 `pip install nonebot-plugin-heweather` 进行安装

然后在 `bot.py` 中 写入 `nonebot.load_plugin("nonebot_plugin_heweather")`

# 指令

`天气+地区` 或 `地区+天气`

# 配置

## apikey 必须配置 环境配置

```
QWEATHER_APIKEY = xxx
```

## 是否使用商业版 可选 环境配置

- 不添加则默认开发版

```
QWEATHER_COMMERCIAL = true
```

## 字体文件 可选 环境配置

```
QWEATHER_FONT = "./data/heweather/font.ttc"
```

- 使用 truetype 字体
- 建议使用微软雅黑

## 图标文件 可选 环境配置

**注意**末端的`/`, 代表目录！

```
QWEATHER_ICON_DIR = "./data/heweather/icon/"
```

## 背景文件 可选 环境配置


默认路径`./data/heweather/backgroud.png`

```
QWEATHER_BACKGROUD = "./data/heweather/backgroud.png"
```


