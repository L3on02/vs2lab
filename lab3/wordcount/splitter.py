import pickle
import time
import zmq
import consts

def read_sentences_from(file_path):
    file  = open(file_path, "r")
    lines = file.readlines()
    file.close()

    return lines

def start_socket():
    src = consts.S
    prt = consts.S_PORT
    
    context = zmq.Context()
    push_socket = context.socket(zmq.PUSH)
    
    address = "tcp://" + src + ":" + prt
    push_socket.bind(address)

    return push_socket

def main():
    push_socket = start_socket()
    
    time.sleep(1)
    
    file_path = "sentences.txt"
    lines     = read_sentences_from(file_path)

    # print(lines)

    for current_line in lines:
        push_socket.send(pickle.dumps(current_line))

if __name__ == "__main__":
    main()