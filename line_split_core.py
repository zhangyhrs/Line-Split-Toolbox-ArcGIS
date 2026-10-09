# -*- coding: utf-8 -*-
from __future__ import division
import os
import re
import math
import arcpy

VERSION = "1.0.0"
RESULT_FIELDS = ["SRC_OID", "SEG_NO", "SEG_M", "START_M", "END_M"]

def parse_lengths(value):
    if value is None:
        raise ValueError("Length sequence is empty.")
    parts = re.split(u"[,，;；、]", unicode(value))
    if not parts or any(not p.strip() for p in parts):
        raise ValueError("Enter positive lengths such as 100,300,150.")
    numbers = []
    for part in parts:
        number = float(part.strip())
        if not (number > 0 and not math.isnan(number) and not math.isinf(number)):
            raise ValueError("All lengths must be positive finite numbers.")
        numbers.append(number)
    return numbers

def check_input(input_lines):
    desc = arcpy.Describe(input_lines)
    if desc.shapeType != "Polyline":
        raise ValueError("Input must be a polyline layer.")
    sr = desc.spatialReference
    if sr is None or sr.type != "Projected" or abs(float(sr.metersPerUnit) - 1.0) > 1e-8:
        raise ValueError("Input must have a metre-based projected coordinate system.")
    return desc

def intervals(total, lengths, repeat):
    if total <= 0:
        return []
    eps = max(total * 1e-12, 1e-9)
    breaks = [0.0]
    pos = 0.0
    i = 0
    while True:
        if not repeat and i >= len(lengths):
            break
        nxt = pos + lengths[i % len(lengths)]
        if nxt >= total - eps:
            break
        breaks.append(nxt)
        pos = nxt
        i += 1
        if i > 1000000:
            raise ValueError("Too many segments for a single feature.")
    breaks.append(total)
    return zip(breaks[:-1], breaks[1:])

def run(input_lines, lengths, repeat, reverse, output_lines):
    desc = check_input(input_lines)
    if not output_lines:
        raise ValueError("Output path required.")
    if os.path.normcase(os.path.abspath(desc.catalogPath)) == os.path.normcase(os.path.abspath(output_lines)):
        raise ValueError("Cannot overwrite the source data.")
    if arcpy.Exists(output_lines):
        raise ValueError("Output already exists. Choose another name.")
    folder, name = os.path.split(output_lines)
    if not folder or not arcpy.Exists(folder):
        raise ValueError("Output workspace does not exist.")
    conflicts = set(f.name.upper() for f in arcpy.ListFields(input_lines)).intersection(RESULT_FIELDS)
    if conflicts:
        raise ValueError("Reserved field(s) already exist: " + ",".join(sorted(conflicts)))
    fields = [f.name for f in arcpy.ListFields(input_lines) if f.type not in ("OID", "Geometry", "Raster", "Blob", "GlobalID") and not f.required and f.editable]
    created = False
    count = 0
    segments = 0
    try:
        arcpy.CreateFeatureclass_management(folder, name, "POLYLINE", input_lines, "SAME_AS_TEMPLATE", "SAME_AS_TEMPLATE", desc.spatialReference)
        created = True
        for field, typ in [("SRC_OID", "LONG"), ("SEG_NO", "LONG"), ("SEG_M", "DOUBLE"), ("START_M", "DOUBLE"), ("END_M", "DOUBLE")]:
            arcpy.AddField_management(output_lines, field, typ)
        with arcpy.da.SearchCursor(input_lines, ["OID@", "SHAPE@"] + fields) as source:
            with arcpy.da.InsertCursor(output_lines, ["SHAPE@"] + fields + RESULT_FIELDS) as target:
                for row in source:
                    oid, geometry = row[0], row[1]
                    if geometry is None or geometry.length <= 0:
                        continue
                    count += 1
                    total = float(geometry.length)
                    for seq, (start, end) in enumerate(intervals(total, lengths, repeat), 1):
                        left, right = (total - end, total - start) if reverse else (start, end)
                        piece = geometry.segmentAlongLine(left, right, False)
                        if piece is None or piece.length <= 0:
                            raise ValueError("Splitting failed for source OID %s." % oid)
                        target.insertRow([piece] + list(row[2:]) + [oid, seq, float(piece.length), float(start), float(end)])
                        segments += 1
                    if count % 100 == 0:
                        arcpy.AddMessage(u"已处理 %s 条线，生成 %s 条分段线。" % (count, segments))
        arcpy.AddMessage(u"完成：处理 %s 条线，生成 %s 条分段线。" % (count, segments))
        arcpy.AddMessage(output_lines)
    except Exception:
        if created and arcpy.Exists(output_lines):
            try:
                arcpy.Delete_management(output_lines)
            except Exception:
                pass
        raise
