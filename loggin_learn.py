# { "op":"add", "path": "/products/pid-00186262", "attribute": {"hasLiveCADDrawing": "Y"}}
# {"op":"add", "path": "/products/pid-123", "value" : {"attribute": {"2":"23","32":"32"}}}

file_o = open("testing.json","w")
p = 123
a = '{"2":"23","32":"32"}'
x = '"op":"add", "path": "/products/pid-{}", "values": {}'

val = "{" +'"attribute":{}'.format(a)+"}"
print(val)
file_o.write("{"+x.format(p,val)+"}")
file_o.close()