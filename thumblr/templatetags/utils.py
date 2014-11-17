def parse_kwargs(kwargs):
    res = {}
    for item in kwargs:
        k, v = item.split(u"=")
        k = remove_quotes(k)
        v = remove_quotes(v)

        if v == u'True':
            res[k] = True
        elif v == u'False':
            res[k] = False
        else:
            res[k] = v

    return res


def remove_quotes(s):
    if s[0] in (u"'", u'"'):
        s = s[1:]
    if s[-1] in (u"'", u'"'):
        s = s[:-1]
    return s