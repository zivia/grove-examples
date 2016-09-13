# automatically generated by the FlatBuffers compiler, do not modify

# namespace: foraging

import flatbuffers

class Behavior(object):
    __slots__ = ['_tab']

    @classmethod
    def GetRootAsBehavior(cls, buf, offset):
        n = flatbuffers.encode.Get(flatbuffers.packer.uoffset, buf, offset)
        x = Behavior()
        x.Init(buf, n + offset)
        return x

    # Behavior
    def Init(self, buf, pos):
        self._tab = flatbuffers.table.Table(buf, pos)

    # Behavior
    def IdBehavior(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(4))
        if o != 0:
            return self._tab.Get(flatbuffers.number_types.Int8Flags, o + self._tab.Pos)
        return 0

def BehaviorStart(builder): builder.StartObject(1)
def BehaviorAddIdBehavior(builder, idBehavior): builder.PrependInt8Slot(0, idBehavior, 0)
def BehaviorEnd(builder): return builder.EndObject()