# ライブラリ
import queue
import socket
import threading
from dataclasses import dataclass
import pygame
from pygame.constants import *

# サイズ設定
WIDTH = 640
HEIGHT = 640

# 色の定義
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

BK_COLOR = WHITE  # 背景色の設定

FPS = 60  # フレーム数設定


def c2s(ip, port, msg):  # サーバー側へ送信
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    serv_address = (ip, port)
    s.sendto(msg.encode('utf-8'), serv_address)


@dataclass
class Client:  # クライアント側処理

    def __init__(self, q):
        self.q = q
        pygame.init()
        pygame.display.set_caption("main")
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.font = pygame.font.Font(None, 55)

    def draw(self):
        loop = True
        text1 = self.font.render("", True, WHITE)
        text2 = self.font.render("", True, WHITE)
        position1 = (1, 1)
        position2 = (1, 1)
        self.screen.fill(BK_COLOR)
        pygame.display.flip()
        while loop:

            for event in pygame.event.get():
                # 「閉じる」ボタンを処理する
                if event.type == pygame.QUIT: loop = False
                if event.type == KEYDOWN:
                    if event.key == 113:
                        loop = False
                    else:
                        self.screen.fill(BK_COLOR)
                        text1 = self.font.render(pygame.key.name(event.key), True, BLACK)
                        c2s("localhost", 2222, pygame.key.name(event.key))
                        position1 = text1.get_rect()
                        position1.left = self.screen.get_rect().left

            if not self.q.empty():
                self.screen.fill(BK_COLOR)
                text2 = self.font.render(self.q.get(), True, BLACK)
                position2 = text2.get_rect()
                position2.right = self.screen.get_rect().right
            self.screen.blit(text1, position1)
            self.screen.blit(text2, position2)
            pygame.display.flip()


class Server:  # サーバー側処理
    def __init__(self, q):
        self.q = q
        self.host = "localhost"
        self.port = 8080
        self.bufsize = 1024

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind((self.host, self.port))
        self.thread = threading.Thread(target=self.c2s, daemon=True)
        self.thread.start()

    def c2s(self):  # サーバー側へ受信
        try:
            while True:
                msg, cli_addr = self.sock.recvfrom(self.bufsize)
                msg.decode('utf-8')
                self.q.put(msg)
                if msg == 'q':
                    break
                # print(msg)
        except Exception as e:
            print(e)

        # self.sock.close()


def main():
    q = queue.Queue()
    client = Client(q)  # 盤面初期化
    server = Server(q)
    client.draw()  # メインルーチン


if __name__ == "__main__":
    main()
