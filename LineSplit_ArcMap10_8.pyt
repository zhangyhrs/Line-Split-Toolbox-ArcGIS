# -*- coding: utf-8 -*-
"""ArcGIS Desktop 10.8 Python 2.7 Toolbox. Version 1.0.0."""
import os
import sys
import arcpy
folder = os.path.dirname(os.path.abspath(__file__))
if folder not in sys.path:
    sys.path.insert(0, folder)
import line_split_core as engine

class Toolbox(object):
    def __init__(self):
        self.label = u"线要素长度分割工具箱 V1.0.0"
        self.alias = "LineSplitToolbox"
        self.tools = [EqualDistanceSplit, CustomDistanceSplit]

def common():
    src = arcpy.Parameter(displayName=u"输入线要素（支持选择集）", name="input_lines", datatype="GPFeatureLayer", parameterType="Required", direction="Input")
    direction = arcpy.Parameter(displayName=u"分割方向", name="split_direction", datatype="GPString", parameterType="Required", direction="Input")
    direction.filter.type = "ValueList"
    direction.filter.list = [u"从起点至终点", u"从终点至起点"]
    direction.value = u"从起点至终点"
    out = arcpy.Parameter(displayName=u"输出线要素类", name="output_lines", datatype="DEFeatureClass", parameterType="Required", direction="Output")
    return src, direction, out

def default_output(ps, index, suffix):
    if ps[0].valueAsText and not ps[index].altered:
        try:
            path = arcpy.Describe(ps[0].valueAsText).catalogPath
            directory, basename = os.path.split(path)
            if directory.lower().endswith((".gdb", ".mdb")):
                path_out = os.path.join(directory, basename + suffix)
            else:
                path_out = os.path.join(directory, os.path.splitext(basename)[0] + suffix + ".shp")
            ps[index].value = path_out
        except Exception:
            pass

def validate(ps, index):
    if ps[0].valueAsText:
        try:
            engine.check_input(ps[0].valueAsText)
        except Exception as exc:
            ps[0].setErrorMessage(unicode(exc))
    if ps[0].valueAsText and ps[index].valueAsText:
        try:
            src = arcpy.Describe(ps[0].valueAsText).catalogPath
            if os.path.normcase(os.path.abspath(src)) == os.path.normcase(os.path.abspath(ps[index].valueAsText)):
                ps[index].setErrorMessage(u"输出不能与输入数据相同。")
        except Exception:
            pass

class EqualDistanceSplit(object):
    def __init__(self):
        self.label = u"01 等距分割线"
        self.description = u"固定长度连续分割，保留最后不足指定长度的线段。"
        self.canRunInBackground = False
    def getParameterInfo(self):
        src, direction, out = common()
        length = arcpy.Parameter(displayName=u"分割长度（米）", name="length_m", datatype="GPDouble", parameterType="Required", direction="Input")
        length.value = 100
        return [src, length, direction, out]
    def updateParameters(self, ps):
        default_output(ps, 3, "_EQ")
    def updateMessages(self, ps):
        validate(ps, 3)
        if ps[1].valueAsText:
            try:
                engine.parse_lengths(ps[1].valueAsText)
            except Exception as exc:
                ps[1].setErrorMessage(unicode(exc))
    def execute(self, ps, messages):
        engine.run(ps[0].valueAsText, engine.parse_lengths(ps[1].valueAsText), True,
                   ps[2].valueAsText == u"从终点至起点", ps[3].valueAsText)

class CustomDistanceSplit(object):
    def __init__(self):
        self.label = u"02 自由长度分割线"
        self.description = u"按不同分段长度顺序切割，可选循环序列。"
        self.canRunInBackground = False
    def getParameterInfo(self):
        src, direction, out = common()
        lengths = arcpy.Parameter(displayName=u"分段长度序列（米，如100,300,150）", name="lengths_m", datatype="GPString", parameterType="Required", direction="Input")
        lengths.value = "100,300,150"
        mode = arcpy.Parameter(displayName=u"序列模式", name="mode", datatype="GPString", parameterType="Required", direction="Input")
        mode.filter.type = "ValueList"
        mode.filter.list = [u"按序列切割一次并保留余段", u"循环重复长度序列"]
        mode.value = u"按序列切割一次并保留余段"
        return [src, lengths, mode, direction, out]
    def updateParameters(self, ps):
        default_output(ps, 4, "_FREE")
    def updateMessages(self, ps):
        validate(ps, 4)
        if ps[1].valueAsText:
            try:
                engine.parse_lengths(ps[1].valueAsText)
            except Exception as exc:
                ps[1].setErrorMessage(unicode(exc))
    def execute(self, ps, messages):
        engine.run(ps[0].valueAsText, engine.parse_lengths(ps[1].valueAsText),
                   ps[2].valueAsText == u"循环重复长度序列",
                   ps[3].valueAsText == u"从终点至起点",
                   ps[4].valueAsText)
