# nonebot-plugin-heweather

获取和风天气信息并转换为图片

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

## 字体文件 可选 环境配置

```
QWEATHER_FONT = "./data/heweather/font.ttc'
```

- 使用 truetype 字体
- 建议使用微软雅黑

## 图标文件 可选 环境配置

**注意**末端的`/`, 代表目录！

```
QWEATHER_ICON_DIR = "./data/heweather/icon/'
```

## 背景文件 可选 环境配置


默认路径`./data/heweather/backgroud.png`

```
QWEATHER_BACKGROUD = "./data/heweather/backgroud.png'
```


