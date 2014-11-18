def get_cdn_domain(file_hash):
    return u"http://static-{num}.unisport.dk".format(
        num=ord(file_hash[-1]) % 10
    )
