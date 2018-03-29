from lark import Lark
import re


# from lark.tree import pydot__tree_to_png  # Just a neat utility function
def pre_compile(source):
    return re.sub(r'(\r?\n)+', '\n', source).lower()


spice_parser = Lark(r"""
    circuits: title definition [commands] end
    title:  NONSENSE ["\r"]"\n"
    definition: ( element | comment )+
    commands: ( command | comment )+
    end:".end" [WS]
    
    comment: "*" NONSENSE (["\r"]"\n") 
    element: (res | cap | vsrc | isrc | induc | vccs | vcvs | ccvs| cccs) ["\r"]"\n"
    command: "." (plot | acdef | dcdef)+ (["\r"]"\n")
    
    res: "r" ELEMENTNAME  pospoint  negpoint value  
    cap: "c" ELEMENTNAME  pospoint negpoint value 
    vsrc: "v" ELEMENTNAME  pospoint negpoint spec
    isrc: "i" ELEMENTNAME  pospoint negpoint value 
    induc: "l" ELEMENTNAME  pospoint negpoint value
    vccs: "g" ELEMENTNAME pospoint negpoint ctlpospnt ctlnegpnt value
    vcvs: "e" ELEMENTNAME pospoint negpoint ctlpospnt ctlnegpnt value
    cccs: "f" ELEMENTNAME pospoint negpoint vname value
    ccvs:"h" ELEMENTNAME pospoint negpoint vname value
    
    spec:   ["dc"] dvalue           ->vdc 
        | "ac" [amag [aphase]] ->vac
    ?dvalue:value
    ?amag:value
    ?aphase:value
    ?pospoint: POINT
    ?negpoint: POINT
    ?ctlpospnt:POINT 
    ?ctlnegpnt:POINT
    ?src1:src
    ?src2:src
    ?fstart: value
    ?fstop: value
    ?start1: value
    ?start2: value
    ?stop1: value
    ?stop2: value
    ?incr1: value
    ?incr2: value

    dcdef: "dc" src1 start1 stop1 incr1 [src2 start2 stop2 incr2]
    acdef: "ac"  [type] pernumber fstart fstop
    type:  "dec"  -> dec
            | "lin" -> lin
            |"oct"  -> oct
    pernumber: INT

    plot: "plot" mode (variable)+
    ?mode: "ac" -> ac
         | "dc" -> dc
    variable: vi [part] "(" pointval ")"
    ?part: "m" -> mag
        |"r" -> real
        |"p"  -> phase 
        |"i" -> img
        |"db" -> db
    ?vi:"v"     -> v
        | "i" -> i
    pointval: POINT            -> valofpoint
            | POINT "," POINT -> difofpoint
            | vi ELEMENTNAME  -> byname
    POINT: INT
    src: vi ELEMENTNAME
    vname: "v" ELEMENTNAME
    value: NUMBER [UNIT]

    NONSENSE:/[^\n]+/
    ELEMENTNAME: /([0-9]|[a-z])+/
    UNIT: "k" | "p" | "n" | "u" | "m" | "f"|"meg"|"g"|"t"|"db" 
    %import common.SIGNED_NUMBER    -> NUMBER
    %import common.INT 
    %import common.WS_INLINE -> W
    %import common.WS -> WS
    %ignore W
""", start='circuits')
