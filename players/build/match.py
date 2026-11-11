import re
STOP={'aaa','aa','a','hockey','club','jr','junior','juniors','elite','academy','hc','the','team','association','major','minor','bantam','premier','national','tier','1','i','t1','u','boys'}
SUB=[(r'\blos angeles\b','la'),(r'\bnew jersey\b','nj'),(r'\bminnesota\b','mn'),(r'\bst\.? louis aaa blues\b','st louis blues'),(r'^reapers\b','chicago reapers'),(r'\bpens\b','penguins'),(r'\bbk selects\b','bishop kearney selects'),(r'^li\b','long island'),(r'\bp\.?a\.?l\.?\b','pal'),(r'\bmid[- ]fairfield\b','midfairfield'),(r'\bhoneybaked\b','hb detroit'),(r'\bmount st\.? charles\b','mount st charles'),(r'\bshattuck[- ]st\.? mary\'?s\b','shattuck st marys'),(r"nor'?easters?",'noreaster'),(r'\bjunior\b','jr')]
def agetag(n):
    m=re.search(r'\b(?:U|M)(\d\d)\b|\b(\d\d)[UO]\b',n,re.I)
    return int(m.group(1) or m.group(2)) if m else None
def norm(n):
    n=n.lower().replace('’',"'")
    for a,b in SUB: n=re.sub(a,b,n)
    n=re.sub(r'\b(?:u|m)\d\d\b|\b\d\d[uo]\b','',n)
    n=re.sub(r"[^a-z0-9 ]",' ',n.replace("'",''))
    return frozenset(t for t in n.split() if t not in STOP)
