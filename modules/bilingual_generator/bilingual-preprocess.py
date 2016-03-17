import itertools
import codecs

d=[]
for entry in a.findall("ar"):
    
    foo = [x.text.split(";") for x in entry if x.text]
    if len(foo) == 2:
        english,hindi = foo
        english = [e.strip() for e in english ]
        hindi = [h.strip() for h in hindi]

        english = [e for e in english if not " " in e]
        hindi = [h for h in hindi if not " " in h]
        for blah in itertools.product(english , hindi):
            d.append(blah)

o = codecs.open('biling', 'w', encoding='utf-8')
for tup in d:
    o.write("%s %s\n" %(tup[0], tup[1]))
o.close()