<div align="center">

# ArcGIS 线要素长度分割工具箱

**ArcGIS 10.8 · 等距分割 · 自由长度分割 · 批量处理**

[🇺🇸 English](./README.md) · [**🇨🇳 中文**](./README_CN.md)

![ArcGIS](https://img.shields.io/badge/ArcGIS-10.8-2470B3?style=flat-square) ![Python](https://img.shields.io/badge/Python-2.7-3776AB?style=flat-square) ![Version](https://img.shields.io/badge/Version-1.0.0-1565C0?style=flat-square) ![License](https://img.shields.io/badge/License-GPL--3.0-00838F?style=flat-square)

</div>

---

## 一、工具简介

**线要素长度分割工具箱**基于 ArcGIS Desktop 10.8、Python 2.7 和 ArcPy 开发，以 Python Toolbox（`.pyt`）形式集成至 ArcToolbox，提供**等距分割线**与**自由长度分割线**两项独立功能。分割长度沿原始线几何计算，结果输出为新的线要素类，不修改输入数据。

## 二、主要功能

| 项目 | 01 等距分割线 | 02 自由长度分割线 |
|---|---|---|
| 输入长度 | 固定长度，如 `100` | 长度序列，如 `100,300,150` |
| 分割模式 | 连续等距切割 | 按顺序一次切割或循环序列 |
| 起止方向 | 起点或终点 | 起点或终点 |
| 末段处理 | 保留余段 | 保留余段 |
| 数据处理 | 支持线要素图层和选择集 | 支持线要素图层和选择集 |
| 输出 | SHP / GDB 线要素类 | SHP / GDB 线要素类 |

自由长度示例：原始线长 **1000 m**，输入 `100,300,150`，选择不循环，则生成 **100 m、300 m、150 m、450 m** 四段。

### 结果字段

| 字段 | 说明 |
|---|---|
| `SRC_OID` | 原始线要素 ObjectID |
| `SEG_NO` | 分段序号 |
| `SEG_M` | 实际计算的线段长度 |
| `START_M` | 当前分割方向上的起始累计里程 |
| `END_M` | 当前分割方向上的终止累计里程 |

## 三、安装与使用

1. 下载仓库 ZIP 并解压至本地文件夹。
2. 将 `LineSplit_ArcMap10_8.pyt` 与 `line_split_core.py` 放在同一目录。
3. 在 ArcMap 10.8 的 **ArcToolbox → Add Toolbox** 中添加 `LineSplit_ArcMap10_8.pyt`。
4. 选择 **01 等距分割线** 或 **02 自由长度分割线**。
5. 设置输入图层、分割长度、方向和输出路径，执行工具。

## 四、使用注意事项

- **坐标系要求：**输入线须采用以米为单位的投影坐标系，按二维投影平面沿线长度分割；不等同于考虑投影变形改正后的地面距离或三维坡面长度。
- **原始数据保护：**输出到新的 SHP 或 GDB 要素类，不能覆盖原始线。
- **质量检查：**正式用于测绘生产前，应重点检查曲线、多部件线、拓扑复杂线、分段长度和属性继承。
- **测试状态：**目前尚未完成 ArcGIS 10.8 实机运行验证，建议先使用测试数据进行验证。

## 五、版本与开源协议

**当前版本：V1.0.0**，适用于 ArcGIS Desktop 10.8，使用 Python 2.7 + ArcPy 开发。

开源协议：[GNU GPL-3.0](./LICENSE)。

---

## Connect / 交流关注

<table align="center">
<tr><th width="33%">WeChat Official Account<br>微信公众号：测绘地信</th><th width="33%">WeChat Mini Program<br>微信小程序：测绘地信</th><th width="33%">Knowledge Planet<br>知识星球：测绘地理信息共享中心</th></tr>
<tr><td align="center"><img src="https://raw.githubusercontent.com/zhangyhrs/GeoStar-Selector-QGIS/main/assets/wechat-official-account.png" alt="WeChat Official Account" height="150"></td><td align="center"><img src="https://raw.githubusercontent.com/zhangyhrs/GeoStar-Selector-QGIS/main/assets/wechat-mini-program.jpg" alt="WeChat Mini Program" height="150"></td><td align="center"><img src="https://raw.githubusercontent.com/zhangyhrs/GeoStar-Selector-QGIS/main/assets/knowledge-planet.jpg" alt="Knowledge Planet" height="150"></td></tr>
</table>

**Author:** Zhang Y.H. · [GitHub @zhangyhrs](https://github.com/zhangyhrs)
