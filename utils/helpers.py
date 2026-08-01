def safe_int(s, default=0):
    try:
        return int(s)
    except:
        return default
