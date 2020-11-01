import multiprocessing 
import traceback
import sys
import os

def sender(conn, fn): 
    """ 
    function to send messages to other end of pipe 
    """
    sys.stdin = os.fdopen(fn)
    try:
        while True:
            msg = input("Input: ")

            conn.send(msg) 
            print("Sent the message: {}".format(msg)) 
    except Exception as e:
        traceback.print_exc()
        conn.close() 
  
def receiver(conn): 
    """ 
    function to print the messages received from other 
    end of pipe 
    """
    while True: 
        msg = conn.recv() 
        if msg == "END": 
            break
        print("Dumped into trash: {}".format(msg)) 
  
if __name__ == "__main__": 
    
    fn = sys.stdin.fileno()
    # creating a pipe 
    parent_conn, child_conn = multiprocessing.Pipe() 
  
    # creating new processes 
    p1 = multiprocessing.Process(target=sender, args=(parent_conn, fn)) 
    p2 = multiprocessing.Process(target=receiver, args=(child_conn,)) 
  
    # running processes 
    p1.start() 
    p2.start() 
  
    # wait until processes finish 
    p1.join() 
    p2.join() 