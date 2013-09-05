import aaf
import aaf.component
from aaf.pct_parser import pct_parser
import array

"""
This example walks through all the video tracks looking for Title_2 OperationGroups 
(these are avid Title Effects, clips a that are created with AvidTitleTool) 
and prints their text, along with the video Track number, in frame and out frame.
"""

def get_video_tracks(mob):
    tracks = []
    
    for slot in mob.slots():
        segment = slot.segment

        if segment.media_kind == "Picture":
            if isinstance(segment, aaf.component.NestedScope):
                
                for nested_segment in segment.segments():
                    
                    if isinstance(nested_segment,  aaf.component.Sequence):
                        tracks.append(list(nested_segment.components()))
                        
            elif isinstance(segment, aaf.component.Sequence):
                tracks.append(list(segment.components()))
                
            elif isinstance(segment, aaf.component.SourceClip):
                tracks.append([segment])

    return tracks

def get_transition_offset(index,component_list):
    
    offset = 0

    nextItem = None
    prevousItem = None
    
    if len(component_list) > index + 1:
        nextItem = component_list[index + 1]
        
    if index != 0:
        prevousItem = component_list[index -1]

    if isinstance(nextItem,  aaf.component.Transition):
        offset -= nextItem.length - nextItem.cutpoint

    if isinstance(prevousItem,  aaf.component.Transition):
        offset -= prevousItem.cutpoint
        
    return offset

def print_text_data(string_data, track_nb, in_frame, out_frame):
    print "Track: V%i Title_2 in: %i out: %i" % (track_nb, in_frame, out_frame)
    data = pct_parser(string_data)
    for item in data:
        if item['type'] == "TitleText":
            print '  ', item['text'].replace("\r",'\n   ')
    

def dump_avid_titles(header):
    
    storage= header.storage()
    
    main_mob = list(storage.toplevel_mobs())[0]
    
    tracks = get_video_tracks(main_mob)
    
    for i, track in enumerate(tracks):

        length = 0
        for k, component in enumerate(track):
            
            transition_offset = get_transition_offset(k,track)
            component_length = component.length + transition_offset
            
            in_frame = length
            out_frame = length +component_length + transition_offset
            
            if isinstance(component,  aaf.component.OperationGroup) and  component.operation == "Title_2":

                for param in component.parameters():
                    if param.name == "AvidGraphicFXAttr":

                        # This parameters value is a iterator object
                        AvidBagOfBits = [v for v in param.value]
                            
                        # convert list of ints to unsigned char data
                        string_data = array.array("B",AvidBagOfBits).tostring()
                        print_text_data(string_data, i+1, in_frame, out_frame)

                if component.has_key("OpGroupGraphicsParamStream"):
                    string_data = component['OpGroupGraphicsParamStream']
                    print_text_data(string_data, i+1, in_frame, out_frame)
                                    
            if not isinstance(component,  aaf.component.Transition):
                length += component_length


if __name__ == "__main__":
    from pprint import pprint
    from optparse import OptionParser
    
    parser = OptionParser()
    (options, args) = parser.parse_args()
    
    
    if not args:
        parser.error("not enough argements")
    
    
    f = aaf.open(args[0])
        
    header = f.header()
        
    dump_avid_titles(header)