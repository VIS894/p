import socket
try:
    s = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    print("socket created")
    ##receiver ke ander ip add receriver ka he aayega
    ## hamesha and  receiver ka he aayega khud ka 
    ip_add = "172.16.4.247"
    port = 8887
    complete_add = (ip_add,port)
    s.bind(complete_add)

    while True:
        message , sender_address = s.recvfrom(1024)
        print("Raw message",message)
        print("sender address", sender_address)
        decoded_msg = message.decode("ascii")
        print("message", decoded_msg)
except Exception as e:
 print("an eroo occured",e)