import pickle
import time
import sys
import string
import zmq
import consts

def start_pull_socket(context, address_of_splitter):
    pull_socket = context.socket(zmq.PULL)
    pull_socket.connect(address_of_splitter)

    return pull_socket

def start_push_socket(context, address_of_reducer):
    push_socket = context.socket(zmq.PUSH)
    push_socket.connect(address_of_reducer)

    return push_socket

def clean_word(word):
    translation_table = str.maketrans("", "", string.punctuation)
    cleaned_word      = word.translate(translation_table)
    
    return cleaned_word

def extract_words_from_lines(lines):
    words = []

    for current_line in lines:
        line_words    = current_line.split()
        cleaned_words = [clean_word(word) for word in line_words]
        words.extend(cleaned_words)

    return words

def main():
    me = str(sys.argv[1])

    red1_addr  = "tcp://" + consts.R1 + ":" + consts.R1_PORT
    red2_addr  = "tcp://" + consts.R2 + ":" + consts.R2_PORT
    split_addr = "tcp://" + consts.S  + ":" + consts.S_PORT

    context = zmq.Context()

    splitter = start_pull_socket(context, split_addr)

    reducer1 = start_push_socket(context, red1_addr)
    reducer2 = start_push_socket(context, red2_addr)

    time.sleep(1)

    is_running = True
    while is_running:
        work  = pickle.loads(splitter.recv())
        lines = work.split()
        words = extract_words_from_lines(lines)

        # Alphabet aufteilen
        # Wörter in der ersten Hälfte zu Reducer 1 
        # und der Rest zu Reducer 2
        for current_word in words:
            first_letter = current_word[0].upper()
            data_to_send = (current_word, me)

            if 'A' <= first_letter <= 'M':
                reducer1.send(pickle.dumps(data_to_send))

            elif 'N' <= first_letter <= 'Z':
                reducer2.send(pickle.dumps(data_to_send))

            else:
                print(f"Error: Invalid first letter = {current_word}")
                #raise ValueError("Invalid first letter: " + current_word)

if __name__ == "__main__":
    main()
#    try: main()

#    except ValueError as ex:
#        print(f"Error: {str(ex)}")