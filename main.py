import pygame
import socket
import threading

def wait_on_connection():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(("127.0.0.1", 44523))
    server_socket.listen(1)
    print("Server waiting on incomig connection")
    conn, address = server_socket.accept()
    print("Connection established")
    return [conn, server_socket]

def hex_to_rgb(hex_code):
    r = int(hex_code[0:2], 16)
    g = int(hex_code[2:4], 16)
    b = int(hex_code[4:6], 16)
    return (r, g, b)

class Screen():
    def clear(self):
        self.disp.fill("black")
        pygame.display.flip()
    def set_pixel(self,x,y,rgb):
        self.disp.set_at((x, y), hex_to_rgb(rgb))
        pygame.display.flip()
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
    def sync_screen(self, displiste):
        self.disp = pygame.init()
        pygame.display.set_mode((255, 255))
        pygame.display.set_caption("AX-10 display")
        self.clock = pygame.time.Clock()
        conn = displiste[0]
        server_socket = displiste[1]
        display = Screen()
        while True:
            commandslist = conn.recv(1024).decode("utf-8").split(" ")
            if commandslist[0] == "0":
                display.clear()
            elif commandslist[0] == "1":
                display.set_pixel(commandslist[1], commandslist[2], commandslist[3])
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    print("Screen closed")
                    pygame.quit()
                    break
            pygame.display.flip()
        conn.close()
        server_socket.close()

if __name__ == "__main__":
    screen = Screen()
    screen.sync_screen(wait_on_connection())