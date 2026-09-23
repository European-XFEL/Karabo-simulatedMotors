# flake8: noqa

from karabo.common.scenemodel.api import (
    ColorBoolModel, DisplayCommandModel, DisplayLabelModel,
    DisplayStateColorModel, DoubleLineEditModel, LabelModel, RectangleModel,
    SceneModel, SceneTargetWindow, write_scene)


def get_scene(deviceId):
    scene00 = RectangleModel(fill='#ffffff', height=271, width=691, x=10, y=10)
    scene01 = DisplayLabelModel(font_size=18, font_weight='bold', height=31, keys=[f'{deviceId}.deviceId'], parent_component='DisplayComponent', width=541, x=30, y=20)
    scene02 = DisplayStateColorModel(font_size=10, font_weight='normal', height=31, keys=[f'{deviceId}.state'], parent_component='DisplayComponent', show_string=True, width=111, x=580, y=20)
    scene03 = RectangleModel(fill='#dcdcdc', height=71, width=561, x=30, y=200)
    scene04 = DisplayCommandModel(font_size=10, height=33, keys=[f'{deviceId}.on'], parent_component='DisplayComponent', width=71, x=600, y=200)
    scene05 = DisplayCommandModel(font_size=10, height=33, keys=[f'{deviceId}.off'], parent_component='DisplayComponent', width=71, x=600, y=233)
    scene06 = RectangleModel(height=81, stroke='#000000', width=161, x=520, y=60)
    scene07 = ColorBoolModel(height=21, invert=True, keys=[f'{deviceId}.isCWLimit'], parent_component='DisplayComponent', width=21, x=640, y=110)
    scene08 = ColorBoolModel(height=21, invert=True, keys=[f'{deviceId}.isSWLimitHigh'], parent_component='DisplayComponent', width=21, x=610, y=110)
    scene09 = LabelModel(font='Source Sans Pro,11,-1,5,50,0,0,0,0,0,Normal', height=21, parent_component='DisplayComponent', text='High Limit', width=81, x=530, y=60)
    scene010 = LabelModel(font='Source Sans Pro,11,-1,5,50,0,0,0,0,0', height=31, parent_component='DisplayComponent', text=' SW', width=41, x=600, y=80)
    scene011 = LabelModel(font='Source Sans Pro,11,-1,5,50,0,0,0,0,0', height=31, parent_component='DisplayComponent', text=' HW', width=41, x=630, y=80)
    scene012 = LabelModel(font='Source Sans Pro,11,-1,5,50,0,0,0,0,0', height=21, parent_component='DisplayComponent', text='Low Limit', width=81, x=33, y=60)
    scene013 = RectangleModel(height=81, stroke='#000000', width=161, x=30, y=60)
    scene014 = ColorBoolModel(height=21, invert=True, keys=[f'{deviceId}.isSWLimitLow'], parent_component='DisplayComponent', width=21, x=83, y=110)
    scene015 = ColorBoolModel(height=21, invert=True, keys=[f'{deviceId}.isCCWLimit'], parent_component='DisplayComponent', width=21, x=43, y=111)
    scene016 = LabelModel(font='Source Sans Pro,11,-1,5,50,0,0,0,0,0', height=31, parent_component='DisplayComponent', text=' HW', width=41, x=33, y=80)
    scene017 = LabelModel(font='Source Sans Pro,11,-1,5,50,0,0,0,0,0', height=31, parent_component='DisplayComponent', text=' SW', width=41, x=73, y=80)
    scene018 = RectangleModel(fill='#dcdcdc', height=41, width=561, x=30, y=150)
    scene019 = LabelModel(font='Source Sans Pro,11,-1,5,50,0,0,0,0,0', foreground='#000000', height=27, parent_component='DisplayComponent', text='Step Size', width=111, x=150, y=157)
    scene020 = DisplayLabelModel(font_size=10, font_weight='normal', height=27, keys=[f'{deviceId}.stepSize'], parent_component='DisplayComponent', width=101, x=260, y=157)
    scene021 = DoubleLineEditModel(decimals=5, height=27, keys=[f'{deviceId}.stepSize'], parent_component='EditableApplyLaterComponent', width=108, x=360, y=157)
    scene022 = DisplayLabelModel(font_size=10, font_weight='normal', height=27, keys=[f'{deviceId}.targetPosition'], parent_component='DisplayComponent', width=101, x=160, y=210)
    scene023 = DisplayLabelModel(font_size=10, font_weight='normal', height=27, keys=[f'{deviceId}.targetVelocity'], parent_component='DisplayComponent', width=101, x=160, y=237)
    scene024 = LabelModel(font='Source Sans Pro,11,-1,5,50,0,0,0,0,0', foreground='#000000', height=27, parent_component='DisplayComponent', text='Target Position', width=111, x=40, y=210)
    scene025 = LabelModel(font='Source Sans Pro,11,-1,5,50,0,0,0,0,0', foreground='#000000', height=27, parent_component='DisplayComponent', text='Velocity', width=111, x=40, y=237)
    scene026 = DisplayCommandModel(font_size=10, height=32, keys=[f'{deviceId}.move'], parent_component='DisplayComponent', width=101, x=450, y=205)
    scene027 = DisplayCommandModel(font_size=10, height=31, keys=[f'{deviceId}.stop'], parent_component='DisplayComponent', width=101, x=450, y=237)
    scene028 = DoubleLineEditModel(decimals=5, height=27, keys=[f'{deviceId}.targetPosition'], parent_component='EditableApplyLaterComponent', width=137, x=260, y=210)
    scene029 = DoubleLineEditModel(decimals=5, height=27, keys=[f'{deviceId}.targetVelocity'], parent_component='EditableApplyLaterComponent', width=121, x=260, y=237)
    scene030 = DisplayLabelModel(font_size=14, font_weight='normal', height=31, keys=[f'{deviceId}.actualPosition'], parent_component='DisplayComponent', width=171, x=330, y=60)
    scene031 = LabelModel(font='Source Sans Pro,11,-1,5,50,0,0,0,0,0', foreground='#000000', height=31, parent_component='DisplayComponent', text='Actual Position', width=121, x=210, y=60)
    scene032 = DisplayCommandModel(font_size=10, height=25, keys=[f'{deviceId}.stepUp'], parent_component='DisplayComponent', width=91, x=40, y=160)
    scene033 = DisplayCommandModel(font_size=10, height=25, keys=[f'{deviceId}.stepDown'], parent_component='DisplayComponent', width=91, x=480, y=160)
    scene = SceneModel(height=293, width=711, children=[scene00, scene01, scene02, scene03, scene04, scene05, scene06, scene07, scene08, scene09, scene010, scene011, scene012, scene013, scene014, scene015, scene016, scene017, scene018, scene019, scene020, scene021, scene022, scene023, scene024, scene025, scene026, scene027, scene028, scene029, scene030, scene031, scene032, scene033])
    return write_scene(scene)

