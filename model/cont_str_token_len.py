def cont_str_token_len(str,cont_len):
    str_token_len=token_count(str)
    if str_token_len>=cont_len:
        while True:
            str=str[:int(len(str)*0.8)]
            if token_count(str)<cont_len:
                return str
    return str