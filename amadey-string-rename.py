#With thanks to OALabs and herrcore for their Amadey stream and notes - https://research.openanalysis.net/cpp/stl/amadey/loader/config/2022/11/13/amadey.html

import ida_bytes
import idautils
import idc
import ida_kernwin

def get_string(addr):
    string_addr = idc.get_operand_value(prev_head(prev_head(addr)), 0)
    string = idc.get_strlit_contents(string_addr, length=-1, strtype=STRTYPE_C)
    if string is None:
        return None
    string = string.decode("UTF-8")
    if ' ' in string:
        string = string.replace(' ', '_')
    if '=' in string:
        string = string.replace('=', '_')
    return string
 
def rename(addr, name):
    name = "g_struct_" + name
    #force_name will automatically put numbers at the end of a name if it's been used already
    ida_name.force_name(addr, name)

def run():
    mw_string_assign = ida_kernwin.ask_long(0x00, "Enter address to string assigning function")
    if mw_string_assign == None:
        ida_kernwin.warning("You did not specify a function address")
        return
    #Get xrefs to string assigning function
    xrefs = set(idautils.CodeRefsTo(mw_string_assign,0))
    if len(xrefs) < 3:
        ida_kernwin.warning("Too little xrefs - did you pick the right function?")
        
    for xref in xrefs:
        #Check if string size is not null
        if idc.get_operand_value(prev_head(prev_head(prev_head(xref))), 0) > 0:
            string = get_string(xref)
            #Calls to string assign that don't match the pattern we described will return None as the string 
            if string is None:
                continue
            #Get offset to stdstring struct that needs to be renamed:
            stdstr_off = idc.get_operand_value(prev_head(xref), 1)
            print("Renaming stdstring struct at:", hex(stdstr_off))
            rename(stdstr_off, string)
        else:
            continue
            
ida_kernwin.add_hotkey("Shift-Y", run)