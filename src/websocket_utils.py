def on_message(data):
    print("recv data: ", data)

def on_error(obj, error):
    print("#################################")
    print("Error: ", error)
    print("#################################")

def on_close(p1, p2, p3):
    print("CLosedd")