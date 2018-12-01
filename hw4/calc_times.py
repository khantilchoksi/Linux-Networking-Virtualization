from collections import defaultdict
f = open("ipf3.txt","r")

c = f.readline()

fn_map = defaultdict(lambda:[0,0])
prev = "NONE"
while c:
        comps = c.split()
        time = comps[0]
        fn_name = comps[1][:comps[1].find("(")]
        fn_map[prev][0] += float(time)
        fn_map[fn_name][1] += 1
        prev = fn_name
        c = f.readline()

for fn_name in fn_map:
        print "Fn ",fn_name," was called ",fn_map[fn_name][1]," times with duration of ",fn_map[fn_name][0]

