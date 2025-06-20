import socket
try:
    ## creating socket
    s = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    #dgram -- datagram
    print("socket created")
    ip_add = "172.16.3.77"
    port =8887
    target_add = (ip_add,port)
    message = input("enter the message : hi😁")
    encoded_msg = message.encode("ascii")
    s.sendto(encoded_msg,target_add)
    print("message sent success")
    s.close()
except Exception as e:
    print("an eroor occured",e)