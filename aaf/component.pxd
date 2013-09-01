cimport lib

from base cimport AAFObject

cdef class Component(AAFObject):
    cdef lib.IAAFComponent *comp_ptr
    
cdef class Segment(Component):
    cdef lib.IAAFSegment *seg_ptr
    
cdef class Transition(Component):
    cdef lib.IAAFTransition *ptr
    
cdef class Sequence(Segment):
    cdef lib.IAAFSequence *ptr
    
cdef class Timecode(Segment):
    pass

cdef class Filler(Segment):
    cdef lib.IAAFFiller *ptr

cdef class Pulldown(Segment):
    pass

cdef class SourceReference(Segment):
    cdef lib.IAAFSourceReference *ref_ptr

cdef class SourceClip(SourceReference):
    cdef lib.IAAFSourceClip *ptr
    
cdef class OperationGroup(Segment):
    cdef lib.IAAFOperationGroup *ptr

cdef class NestedScope(Segment):
    cdef lib.IAAFNestedScope *ptr

cdef class ScopeReference(Segment):
    cdef lib.IAAFScopeReference *ptr

cdef class EssenceGroup(Segment):
    cdef lib.IAAFEssenceGroup *ptr
    
cdef class Selector(Segment):
    cdef lib.IAAFSelector *ptr
    
cdef class Edgecode(Segment):
    pass
    
cdef class Event(Segment):
    cdef lib.IAAFEvent *event_ptr
    
cdef class CommentMarker(Event):
    cdef lib.IAAFCommentMarker *comment_ptr
    
cdef class DescriptiveMarker(CommentMarker):
    cdef lib.IAAFDescriptiveMarker *ptr

cdef class GPITrigger(Event):
    pass
    
cdef class TimecodeStream(Segment):
    pass
    
cdef class TimecodeStream12M(TimecodeStream):
    pass