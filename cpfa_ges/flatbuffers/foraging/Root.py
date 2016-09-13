# automatically generated by the FlatBuffers compiler, do not modify

# namespace: foraging

import flatbuffers

class Root(object):
    __slots__ = ['_tab']

    @classmethod
    def GetRootAsRoot(cls, buf, offset):
        n = flatbuffers.encode.Get(flatbuffers.packer.uoffset, buf, offset)
        x = Root()
        x.Init(buf, n + offset)
        return x

    # Root
    def Init(self, buf, pos):
        self._tab = flatbuffers.table.Table(buf, pos)

    # Root
    def Init(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(4))
        if o != 0:
            x = self._tab.Indirect(o + self._tab.Pos)
            from .Initialization import Initialization
            obj = Initialization()
            obj.Init(self._tab.Bytes, x)
            return obj
        return None

    # Root
    def DefaultBehavior(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(6))
        if o != 0:
            x = self._tab.Indirect(o + self._tab.Pos)
            from .Behavior import Behavior
            obj = Behavior()
            obj.Init(self._tab.Bytes, x)
            return obj
        return None

    # Root
    def Rules(self, j):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(8))
        if o != 0:
            x = self._tab.Vector(o)
            x += flatbuffers.number_types.UOffsetTFlags.py_type(j) * 4
            x = self._tab.Indirect(x)
            from .Rule import Rule
            obj = Rule()
            obj.Init(self._tab.Bytes, x)
            return obj
        return None

    # Root
    def RulesLength(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(8))
        if o != 0:
            return self._tab.VectorLen(o)
        return 0

def RootStart(builder): builder.StartObject(3)
def RootAddInit(builder, init): builder.PrependUOffsetTRelativeSlot(0, flatbuffers.number_types.UOffsetTFlags.py_type(init), 0)
def RootAddDefaultBehavior(builder, defaultBehavior): builder.PrependUOffsetTRelativeSlot(1, flatbuffers.number_types.UOffsetTFlags.py_type(defaultBehavior), 0)
def RootAddRules(builder, rules): builder.PrependUOffsetTRelativeSlot(2, flatbuffers.number_types.UOffsetTFlags.py_type(rules), 0)
def RootStartRulesVector(builder, numElems): return builder.StartVector(4, numElems, 4)
def RootEnd(builder): return builder.EndObject()