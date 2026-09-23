# flake8: noqa

from karabo.common.scenemodel.api import (
    ColorBoolModel, DisplayCommandModel, DisplayLabelModel,
    DisplayStateColorModel, DoubleLineEditModel, LabelModel, RectangleModel,
    SceneModel, SceneTargetWindow, write_scene)


def get_scene(deviceId):
    scene00 = RectangleModel(fill='#ffffff', height=221, width=691, x=10, y=10)
    scene01 = DisplayLabelModel(font_size=18, font_weight='bold', height=31, keys=['SIMMOT.deviceId'], parent_component='DisplayComponent', width=541, x=30, y=20)
    scene02 = DisplayStateColorModel(font_size=10, font_weight='normal', height=31, keys=['SIMMOT.state'], parent_component='DisplayComponent', show_string=True, width=111, x=580, y=20)
    scene03 = RectangleModel(fill='#dcdcdc', height=71, width=561, x=70, y=150)
    scene04 = RectangleModel(height=81, stroke='#000000', width=161, x=520, y=60)
    scene05 = ColorBoolModel(height=21, invert=True, keys=['SIMMOT.isCWLimit'], parent_component='DisplayComponent', width=21, x=640, y=110)
    scene06 = ColorBoolModel(height=21, invert=True, keys=['SIMMOT.isSWLimitHigh'], parent_component='DisplayComponent', width=21, x=610, y=110)
    scene07 = LabelModel(font='Source Sans Pro,11,-1,5,50,0,0,0,0,0,Normal', height=21, parent_component='DisplayComponent', text='High Limit', width=81, x=530, y=60)
    scene08 = LabelModel(font='Source Sans Pro,11,-1,5,50,0,0,0,0,0', height=31, parent_component='DisplayComponent', text=' SW', width=41, x=600, y=80)
    scene09 = LabelModel(font='Source Sans Pro,11,-1,5,50,0,0,0,0,0', height=31, parent_component='DisplayComponent', text=' HW', width=41, x=630, y=80)
    scene010 = LabelModel(font='Source Sans Pro,11,-1,5,50,0,0,0,0,0', height=21, parent_component='DisplayComponent', text='Low Limit', width=81, x=33, y=60)
    scene011 = RectangleModel(height=81, stroke='#000000', width=161, x=30, y=60)
    scene012 = ColorBoolModel(height=21, invert=True, keys=['SIMMOT.isSWLimitLow'], parent_component='DisplayComponent', width=21, x=83, y=110)
    scene013 = ColorBoolModel(height=21, invert=True, keys=['SIMMOT.isCCWLimit'], parent_component='DisplayComponent', width=21, x=43, y=111)
    scene014 = LabelModel(font='Source Sans Pro,11,-1,5,50,0,0,0,0,0', height=31, parent_component='DisplayComponent', text=' HW', width=41, x=33, y=80)
    scene015 = LabelModel(font='Source Sans Pro,11,-1,5,50,0,0,0,0,0', height=31, parent_component='DisplayComponent', text=' SW', width=41, x=73, y=80)
    scene016 = DisplayLabelModel(font_size=10, font_weight='normal', height=27, keys=['SIMMOT.targetPosition'], parent_component='DisplayComponent', width=101, x=200, y=160)
    scene017 = LabelModel(font='Source Sans Pro,11,-1,5,50,0,0,0,0,0', foreground='#000000', height=27, parent_component='DisplayComponent', text='Target Position', width=111, x=80, y=160)
    scene018 = DisplayCommandModel(font_size=10, height=32, keys=['SIMMOT.move'], parent_component='DisplayComponent', width=101, x=490, y=155)
    scene019 = DisplayCommandModel(font_size=10, height=31, keys=['SIMMOT.stop'], parent_component='DisplayComponent', width=101, x=490, y=187)
    scene020 = DoubleLineEditModel(decimals=5, height=27, keys=['SIMMOT.targetPosition'], parent_component='EditableApplyLaterComponent', width=137, x=300, y=160)
    scene021 = DisplayLabelModel(font_size=14, font_weight='normal', height=31, keys=['SIMMOT.actualPosition'], parent_component='DisplayComponent', width=171, x=330, y=60)
    scene022 = LabelModel(font='Source Sans Pro,11,-1,5,50,0,0,0,0,0', foreground='#000000', height=31, parent_component='DisplayComponent', text='Actual Position', width=121, x=210, y=60)
    scene = SceneModel(height=240, width=712, children=[scene00, scene01, scene02, scene03, scene04, scene05, scene06, scene07, scene08, scene09, scene010, scene011, scene012, scene013, scene014, scene015, scene016, scene017, scene018, scene019, scene020, scene021, scene022])
    return write_scene(scene)

