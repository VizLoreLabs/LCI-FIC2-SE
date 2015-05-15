from itertools import islice

LG = 150


def chunks(data, size):
    it = iter(data)
    for k in xrange(0, len(data), size):
        yield {k: data[k] for k in islice(it, size)}


k = [x for x in range(0, LG)]
v = [x for x in range(0, LG)]

d = dict()

for i in range(0, LG):
    d[k[i]] = v[i]


size = ( len(d) / 10 ) + 1
n_d = chunks(d, size)

o = [i for i in n_d]
print o
