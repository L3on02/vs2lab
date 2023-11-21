import os
import pickle
import sys
import time
from collections import defaultdict
import zmq
import consts

def print_dictionary(dictionary_to_print):
    for key, value in dictionary_to_print.items():
        # print(key + ": " + value) # -> TypeError
        print(f"{key}: {value}")

def start_socket(me):
    src = consts.R1      if me == '1' else consts.R2
    prt = consts.R1_PORT if me == '1' else consts.R2_PORT

    context = zmq.Context()

    pull_socket = context.socket(zmq.PULL)
    pull_socket.bind("tcp://" + src + ":" + prt)

    return pull_socket

def process_data(pull_socket, me):
    dict_counted_words = defaultdict(int)

    is_running = True

    try:
        while is_running:
            word, mapper_id = pickle.loads(pull_socket.recv())

            dict_counted_words[word] += 1

            print("------------------------------")
            print(f"From mapper {mapper_id} {os.linesep}Current dictionary for reducer {me}")
            print_dictionary(dict_counted_words)

            time.sleep(1)

    except KeyboardInterrupt: pass

    return dict_counted_words

def main():
    me          = str(sys.argv[1])
    pull_socket = start_socket(me)

    print("{} started".format(me))

    dict_counted_words = {0,0}
    try:
        dict_counted_words = process_data(pull_socket, me)

    finally:
        # Terminal aufräumen
        os.system("cls" if os.name == "nt" else "clear")

        # Finale Ausgabe
        print(f"Final dictionary for reducer {me}")
        print_dictionary(dict_counted_words)

if __name__ == "__main__":
    main()