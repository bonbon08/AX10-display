from tkinter import *
import socket

def wait_on_connection():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(("127.0.0.1", 44523))
    server_socket.listen(1)
    print("Server waiting on incoming connection")
    conn, address = server_socket.accept()
    print("Connection established")
    return [conn, server_socket]

def hex_to_rgb(hex_code):
    r = int(hex_code[0:2], 16)
    g = int(hex_code[2:4], 16)
    b = int(hex_code[4:6], 16)
    return (r, g, b)

class Screen():
    def __init__(self):
        self.window = Tk()
        self.canvas_place = Canvas(self.window, width=255, height=255, bd=0, highlightthickness=0, relief='ridge')
        self.canvas_place.pack()
        self.clear()
    def clear(self):
        self.canvas_place.create_rectangle(0, 0, 255, 255, fill="#000000", outline="#000000")
    def set_char(self,x,y,char):
        index1 = 0
        index2 = 0
        for i in char:
            for s in i:
                if s == 1:
                    self.disp.set_at((x+index2, y+index1), (0, 0, 0))
                index2 += 1
            index2 = 0
            index1 += 1
        pygame.display.flip()

    def sync_screen(self, conn):
        allcoms = []
        while True:
            try:
                commandstring = conn.recv(2048).decode("utf-8")
                allcoms.append(commandstring)
                if allcoms != [""]:
                    while len(allcoms) > 0:
                        commandstring = allcoms.pop().split("!")
                        for command in commandstring:
                            commandslist = command.split(" ")
                            if commandslist[0] == "0" and commandslist[1] == "0" and commandslist[3] == "0":
                                self.clear()
                            elif commandslist[0] == "1":
                                self.canvas_place.create_rectangle(int(commandslist[1]), int(commandslist[2]), (int(commandslist[1])+1), (int(commandslist[2])+1), fill="#"+commandslist[3], outline="#"+commandslist[3])
                            self.window.update()
            except Exception as error:
                print(error)

if __name__ == "__main__":
    screen = Screen()
    conn, server_socket = wait_on_connection()
    screen.sync_screen(conn)
    pygame.quit()
