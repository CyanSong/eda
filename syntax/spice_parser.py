import re

from lark import Lark


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
    element: (res | cap | vsrc | isrc | induc | vccs | vcvs | ccvs| cccs |diode | mos) ["\r"]"\n"
    command: "." (plot | acdef | dcdef | trandef| print )+ (["\r"]"\n")
    
    res: "r" ELEMENTNAME  pospoint  negpoint value  
    cap: "c" ELEMENTNAME  pospoint negpoint value 
    vsrc: "v" ELEMENTNAME  pospoint negpoint spec
    isrc: "i" ELEMENTNAME  pospoint negpoint value 
    induc: "l" ELEMENTNAME  pospoint negpoint value
    vccs: "g" ELEMENTNAME pospoint negpoint ctlpospnt ctlnegpnt value
    vcvs: "e" ELEMENTNAME pospoint negpoint ctlpospnt ctlnegpnt value
    cccs: "f" ELEMENTNAME pospoint negpoint vname value
    ccvs:"h" ELEMENTNAME pospoint negpoint vname value
    mos: "m" ELEMENTNAME dpoint gpoint spoint bpoint mosmodel ["l="l] ["w="w]
    diode:"d" ELEMENTNAME pospoint negpoint modelname [area] ["off"] ["ic="vd] 
    dcdef: "dc" dsrc1 [dsrc2]
    acdef: "ac"  [type] pernumber fstart fstop
    trandef: "tran" incr stop [start [max_int]]
    plot: "plot" mode (variable)+
    print: "print" mode (variable)+
    

    modelname:"model1"  
            | "model2" 
    mosmodel:"nm" ->nmos
            |"pm" ->pmos
    spec:   ["dc"] dvalue           ->vdc 
        | "ac" [amag [aphase]] ->vac
        | "sin" "("  v0   va  freq td  theta  ")" ->sin
        | "pulse" "(" v1 v2  td tr tf pw per ")" ->pulse
    dsrc:src start stop incr
    type:  "dec"  -> dec
            | "lin" -> lin
            |"oct"  -> oct
    pernumber: INT
    ?mode: "ac" -> ac
     | "dc" -> dc
     | "tran" ->tran
    variable: vi [part] "(" pointval ")"
    pointval: POINT            -> valofpoint
            | POINT "," POINT -> diffofpoint
            | elemtype ELEMENTNAME  -> byname
    
    ?elemtype:   "r" ->r
               | "c" ->c
               | "v" ->v
               | "i" ->i
               | "l" ->l
               | "g" ->g
               | "e" ->e
               | "f" ->f
               | "h" ->h
               | "d" ->d
    
    
    POINT: INT
    src: vi ELEMENTNAME
    value: NUMBER [UNIT]
    ?part: "m" -> mag
    |"r" -> real
    |"p"  -> phase 
    |"i" -> img
    |"db" -> db
    ?vi:"v"     -> v
        | "i" -> i
    vname: "v" ELEMENTNAME
    
    NONSENSE:/[^\n]+/
    ELEMENTNAME: /([0-9]|[a-z])+/

    
    UNIT: "k" | "p" | "n" | "u" | "m" | "f"|"meg"|"g"|"t"|"db" 
    ?l:value
    ?w:value
    ?freq:value
    ?area: value
    ?vd: value
    ?v0:value
    ?va:value
    ?td:value
    ?v1:value
    ?v2:value
    ?tf:value
    ?tr:value
    ?pw:value
    ?per:value
    ?theta:value  
    ?dvalue:value
    ?amag:value
    ?aphase:value
    ?pospoint: POINT
    ?negpoint: POINT
    ?dpoint:POINT
    ?gpoint:POINT
    ?spoint:POINT
    ?bpoint:POINT
    ?ctlpospnt:POINT 
    ?ctlnegpnt:POINT
    ?fstart: value
    ?fstop: value
    ?start: value
    ?stop: value
    ?incr: value
    ?max_int : value
    ?dsrc1:dsrc
    ?dsrc2:dsrc

    %import common.SIGNED_NUMBER    -> NUMBER
    %import common.INT 
    %import common.WS_INLINE -> W
    %import common.WS -> WS
    %ignore W
""", start='circuits')
