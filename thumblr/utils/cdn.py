def get_cdn_domain(file_hash):
    if not file_hash:
        return None

    num = ord(file_hash[-1]) % 10
    return u"http://static-{num}.unisport.dk".format(
        num=num,
    )
