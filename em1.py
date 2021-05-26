import sys
import Conn_mariadb


def cont(conn):
    # update subject
    prompt1 = input('Update subject y/n?: ')
    if prompt1.startswith('y'):
        new_value = input('New value : ')
        print(conn.update_keyvalue(new_value, "subject"))
    # update message
    prompt1 = input('Update message y/n?: ')
    if prompt1.startswith('y'):
        new_value = input('New value : ')
        print(conn.update_keyvalue(new_value, "message"))
    # send emails
    prompt1 = input('Send email y/n?: ')
    if prompt1.startswith('y'):
        print(conn.send_one())
    else:
        print('quitting')
        sys.exit(0)

def main(dirty=True):
    """  main """
    conn = Conn_mariadb.Conn_mariadb('clients')

    if dirty:
        print('Welcome ...q Quits')
        dirty = False

    if not dirty:
        print(conn.select_to_list())
        prompt1 = input('Add y/n/q ?: ')
        if prompt1.startswith('y'):
            prompt2 = input("First name: ")
            prompt3 = input("Email : ")
            res = conn.add_client(prompt2, prompt3)
            if res.lower().startswith('a'):
                prompt4 = input('try again? y/n?: ')
                if prompt4.startswith('y'):
                    prompt4 = None
                    main(False)
            else:
                main(False)
        elif prompt1.startswith('q'):
            print("bye...")
            sys.exit(0)
        else:
            cont(conn)

if __name__ == '__main__':
    main()
   
