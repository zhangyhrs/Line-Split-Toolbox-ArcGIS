<div align="center">

# Line Split Toolbox for ArcGIS

**Equal-distance and custom-length polyline segmentation for ArcGIS Desktop 10.8**

[**🇺🇸 English**](./README.md) · [🇨🇳 中文](./README_CN.md)

![ArcGIS](https://img.shields.io/badge/ArcGIS-10.8-2470B3?style=flat-square) ![Python](https://img.shields.io/badge/Python-2.7-3776AB?style=flat-square) ![Version](https://img.shields.io/badge/Version-1.0.0-1565C0?style=flat-square) ![License](https://img.shields.io/badge/License-GPL--3.0-00838F?style=flat-square)

</div>

---

## Overview

**Line Split Toolbox** is a Python Toolbox (`.pyt`) for ArcMap 10.8, supporting both fixed-distance and variable-distance line segmentation. The tool computes distances **along the polyline**, preserves source attributes, and writes a separate output dataset.

## Features

- **01 Equal-distance split:** split a line into fixed lengths such as 100 m each, retaining any remaining part.
- **02 Custom-length split:** enter a sequence like `100,300,150` and split in the specified order.
- **Modes:** split the custom sequence once, or repeat it until reaching the end.
- **Direction:** split from start to end, or from end to start.
- **Batch processing:** operate on a polyline feature layer, including its active selection.
- **Outputs:** SHP or file geodatabase feature class with original editable attributes and added tracking fields.

## Quick example

For a 1,000 m line, entering `100,300,150` in non-repeating mode yields **100 m + 300 m + 150 m + 450 m**.

| Output field | Description |
|---|---|
| `SRC_OID` | Source feature's ObjectID |
| `SEG_NO` | Segment sequence number |
| `SEG_M` | Measured segment length |
| `START_M` | Cumulative start distance in selected direction |
| `END_M` | Cumulative end distance in selected direction |

## Installation

1. Download the repository as ZIP and extract it to a local folder.
2. Keep `LineSplit_ArcMap10_8.pyt` and `line_split_core.py` **in the same directory**.
3. Open **ArcMap 10.8 → ArcToolbox → Add Toolbox**.
4. Select `LineSplit_ArcMap10_8.pyt` and open either tool.
5. Set your input polyline layer, splitting parameters, and output path; then run.

## Repository layout

```text
Line-Split-Toolbox-ArcGIS/
├── LineSplit_ArcMap10_8.pyt
├── line_split_core.py
├── README.md
├── README_CN.md
├── .gitignore
└── LICENSE
```

## Notes

- Input data must be in a **projected coordinate system with metre units**. The algorithm uses 2D planar length along the source polyline, not slope distance or ground-distance corrected for projection distortion.
- The source dataset is not modified. Choose a new output name.
- Splitting curved, multipart or topologically complex lines should be verified against the required production rules.
- **ArcMap runtime validation is still required.** The source is provided for testing and review; a passing ArcGIS 10.8 production test is not claimed.

## Version & License

**Version: 1.0.0** · Python 2.7 / ArcPy / ArcGIS Desktop 10.8

Licensed under [GNU GPL-3.0](./LICENSE).

---

## Connect / 交流关注

<table align="center">
<tr><th width="33%">WeChat Official Account<br>微信公众号：测绘地信</th><th width="33%">WeChat Mini Program<br>微信小程序：测绘地信</th><th width="33%">Knowledge Planet<br>知识星球：测绘地理信息共享中心</th></tr>
<tr><td align="center"><img src="https://raw.githubusercontent.com/zhangyhrs/GeoStar-Selector-QGIS/main/assets/wechat-official-account.png" alt="WeChat Official Account" height="150"></td><td align="center"><img src="https://raw.githubusercontent.com/zhangyhrs/GeoStar-Selector-QGIS/main/assets/wechat-mini-program.jpg" alt="WeChat Mini Program" height="150"></td><td align="center"><img src="https://raw.githubusercontent.com/zhangyhrs/GeoStar-Selector-QGIS/main/assets/knowledge-planet.jpg" alt="Knowledge Planet" height="150"></td></tr>
</table>

**Author:** Zhang Y.H. · [GitHub @zhangyhrs](https://github.com/zhangyhrs)
