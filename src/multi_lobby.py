import pygame, setting, socket
from menu import Menu
from button import Button
from constant import *

#######################
# 멀티플레이 state 설명
# client_or_server: 클라이언트인지 서버인지 설정하는 부분
# client_connection: 클라이언트가 ip를 입력하고 접속하려 하는 부분
# client_password: 클라이언트가 비밀번호를 입력하는 부분
# client_connected: 서버에 접속한 이후 클라이언트의 시점
# server_connected: 서버가 생성된 이후 서버의 시점
#######################
class MultiLobby(Menu):
    # 가능한 메뉴 목록
    other = []
    name = "My Name"
    password = ""
    # 우선 서버라고 가정하고, 클라이언트면 서버의 값을 덮어씌우기
    host_ip = socket.gethostbyname(socket.gethostname())

    state = "client_or_server"
    # 버튼이 있어야 할 위치 반환
    get_position = lambda self, index: (
        self.pos[0],
        self.pos[1] + self.size[1] * 1.2 * index,
    )

    def __init__(self, pos=(0, 0), size=(150, 50)):
        self.avail_menu = ["CLIENT", "SERVER", "BACK"]

        self.menu = self.avail_menu
        self.max_menu = len(self.menu)
        self.max_other = len(self.other)
        self.button = []
        self.rect = []
        self.pos = pos
        self.size = size
        self.pressed = False
        self.other_chk = [True, False, False, False, False]

        # 현재 highlight된 위치의 index
        self.highlight = 0
        # 현재 선택된 대상, -1일 경우 마우스 조작 중
        self.selected = -1
        self.init_draw()

    def init_draw(self):
        self.button = []
        self.rect = []

        for i in range(self.max_other):
            # 버튼 삽입
            if self.other_chk[i] == True:
                image = pygame.image.load(RESOURCE_PATH / "single" / "list.png")
                text = self.other[i]
                color = "White"
            else:
                image = pygame.image.load(
                    RESOURCE_PATH / "single" / "list_unpicked.png"
                )
                text = "+"
                color = "Black"
            self.button.append(
                Button(
                    image,
                    image,
                    pos=(self.size[0] * 7 / 8, self.size[1] * (2 * i + 3) / 12),
                    text_input=text,
                    font=setting.get_font(50),
                    base_color=color,
                    hovering_color=color,
                )
            )
            # 각 버튼 이벤트 처리용 Rect 삽입
            self.rect.append(self.button[i].rect)

        for i in range(self.max_menu):
            # 버튼 삽입
            self.button.append(
                Button(
                    pygame.image.load(RESOURCE_PATH / "main" / "main_button.png"),
                    pygame.image.load(
                        RESOURCE_PATH / "main" / "main_button_highlight.png"
                    ),
                    pos=(self.size[0] / 2, self.size[1] * (2 * i + 13) / 20),
                    text_input=self.menu[i],
                    font=setting.get_font(50),
                    base_color="#3a4aab",
                    hovering_color="White",
                )
            )
            # 각 버튼 이벤트 처리용 Rect 삽입
            self.rect.append(self.button[i + self.max_other].rect)

            # 본인 이름 표시
            self.text_name = setting.get_font(50).render(self.name, True, "White")
            self.text_name_rect = self.text_name.get_rect(
                center=(self.size[0] / 2, self.size[1] * 0.3)
            )

            # 서버 IP 표시
            self.ip_text_name = setting.get_font(50).render(f"IP: {self.host_ip}", True, "White")
            self.ip_text_name_rect = self.ip_text_name.get_rect(
                center=(self.size[0] / 2, self.size[1] * 0.4)
            )

            # 비밀번호 표시
            self.passwd_text_name = setting.get_font(50).render(f"Password Required: {self.password}", True, "White")
            self.passwd_text_name_rect = self.passwd_text_name.get_rect(
                center=(self.size[0] / 2, self.size[1] * 0.4)
            )

    # 크기 변경에 맞춰 재조정
    def resize(self, size):
        self.size = size
        self.init_draw()

    # 스크린에 자신을 그리기
    def draw(self, screen):
        for i in range(self.max_other + self.max_menu):
            self.button[i].update(screen)
            # 컴퓨터 추가 영역 호버링 중지
            if i == self.highlight and i >= self.max_other:
                self.button[i].changeHighlight(True, screen)
            else:
                if i >= self.max_other:
                    self.button[i].changeHighlight(False, screen)

        # Add a Player 텍스트
        if self.state == "server_connected":
            font = setting.get_font(50)
            text_player = font.render("Add a Player", True, "White")
            text_player_rect = text_player.get_rect(
                center=(self.size[0] * 7 / 8, self.size[1] / 12)
            )
            screen.blit(
                text_player,
                text_player_rect,
            )

        # 본인 이름 표시
        if self.state in ("client_connected", "server_connected"):
            screen.blit(
                self.text_name,
                self.text_name_rect,
            )

        # 서버 IP 표시
        if self.state in ("client_connecting", "client_connected", "server_connected"):
            screen.blit(
                self.ip_text_name,
                self.ip_text_name_rect,
            )
        
        # 비밀번호 표시
        if self.state in ("client_password"):
            screen.blit(
                self.passwd_text_name,
                self.passwd_text_name_rect,
            )

    # 메뉴 선택 시 처리
    def select_menu(self, index):
        se_event = pygame.event.Event(
            EVENT_PLAY_SE, {"path": RESOURCE_PATH / "sound" / "button.mp3"}
        )
        pygame.event.post(se_event)

        list_x = 480 * setting.get_screen_scale()
        list_y = 180 * setting.get_screen_scale()

        if index < self.max_other:
            if self.other_chk[index] == True:
                self.button[index].ChangeImage(
                    pygame.transform.scale(
                        pygame.image.load(RESOURCE_PATH / "single" / "list_unpicked.png"),
                        (list_x, list_y)
                    )
                )
                self.button[index].ChangeText("+", "Black", "Black")
                self.other_chk[index] = False
            else:
                self.button[index].ChangeImage(
                    pygame.transform.scale(
                        pygame.image.load(RESOURCE_PATH / "single" / "list.png"),
                        (list_x, list_y)
                    )
                )
                self.button[index].ChangeText(self.other[index], "White", "White")
                self.other_chk[index] = True
        else:
            index -= self.max_other
            if self.avail_menu[index] == "RENAME":
                pygame.event.post(pygame.event.Event(EVENT_OPEN_RENAME))  # 이름 변경
            elif self.avail_menu[index] == "PASSWORD":
                if self.state == "server_connected":
                    # server_connected: 비밀번호 변경
                    pygame.event.post(pygame.event.Event(EVENT_OPEN_HOST_PASSWORD))
                else:
                    # client_password: 비밀번호 입력
                    pygame.event.post(pygame.event.Event(EVENT_OPEN_CLIENT_PASSWORD))
            elif self.avail_menu[index] == "IP":
                # client_connecting: IP 변경
                pygame.event.post(pygame.event.Event(EVENT_OPEN_ENTER_IP))
            elif self.avail_menu[index] == "SERVER":
                # client_or_server: 서버 선택
                self.host_ip = socket.gethostbyname(socket.gethostname())
                self.state = "server_connected"
                self.other = ["1", "2", "3", "4", "5"]
                self.max_other = 5
                self.avail_menu = ["RENAME", "PASSWORD", "START", "BACK"]
                self.menu = self.avail_menu
                self.max_menu = 4
                self.init_draw()
            elif self.avail_menu[index] == "CLIENT":
                # client_or_server: 클라이언트 선택
                if self.state == "client_or_server":
                    self.host_ip = ""
                    self.state = "client_connecting"
                    self.avail_menu = ["IP", "CONNECT", "BACK"]
                    self.menu = self.avail_menu
                    self.max_menu = 3
                    self.init_draw()
            elif self.avail_menu[index] == "CONNECT":
                # client_connecting: 접속 시도 -> 비밀번호 입력
                self.host_ip = ""
                # TODO: 실제로 서버와 연결해서 비밀번호 필요 여부 확인
                if True: # TODO: 비밀번호가 필요하다면
                    self.password = ""
                    self.state = "client_password"
                    self.avail_menu = ["PASSWORD", "JOIN", "BACK"]
                    self.menu = self.avail_menu
                    self.max_menu = 3
                    self.init_draw()
                else:
                    pass
            elif self.avail_menu[index] == "JOIN":
                # client_password: 비밀번호 입력 -> 접속
                # TODO: 서버와 통신하여 비밀번호 검증
                if True: # TODO: 비밀번호가 일치한다면
                    # TODO: 정원 초과를 확인해서 오류 메시지 표시
                    self.host_ip = socket.gethostbyname(socket.gethostname())
                    self.state = "client_connected"
                    # TODO: 서버와 통신하여 타 플레이어 정보 받아오기
                    self.other = ["1", "2", "3", "4", "5"]
                    self.max_other = 5
                    self.avail_menu = ["RENAME", "BACK"]
                    self.menu = self.avail_menu
                    self.max_menu = 2
                    self.init_draw()
                else:
                    print("비밀번호가 틀렸습니다.")
            elif self.avail_menu[index] == "START":
                # server_connected: 게임 시작
                if self.other_chk.count(True) == 0:
                    pass
                else:
                    # pygame.event.post(pygame.event.Event(EVENT_START_SINGLE))
                    # TODO: 멀티플레이 게임 시작
                    pass
            elif self.avail_menu[index] == "BACK":
                if self.state == "client_or_server":
                    pygame.event.post(pygame.event.Event(EVENT_MAIN))  # 메인 메뉴
                elif self.state == "client_connecting":
                    self.state = "client_or_server"
                    self.avail_menu = ["CLIENT", "SERVER", "BACK"]
                    self.menu = self.avail_menu
                    self.max_menu = 3
                    self.init_draw()
                elif self.state == "client_password":
                    self.state = "client_connecting"
                    self.avail_menu = ["IP", "CONNECT", "BACK"]
                    self.menu = self.avail_menu
                    self.max_menu = 3
                    self.init_draw()
                elif self.state == "server_connected":
                    # TODO: 방에 들어온 인원 전원 강퇴
                    self.state = "client_or_server"
                    self.other = []
                    self.max_other = 0
                    self.avail_menu = ["CLIENT", "SERVER", "BACK"]
                    self.menu = self.avail_menu
                    self.max_menu = 3
                    self.init_draw()
                elif self.state == "client_connected":
                    # TODO: 방장에게 방 떠남을 알리기
                    self.state = "client_or_server"
                    self.other = []
                    self.max_other = 0
                    self.avail_menu = ["CLIENT", "SERVER", "BACK"]
                    self.menu = self.avail_menu
                    self.max_menu = 3
                    self.init_draw()
            
    # 이벤트 처리
    def handle_event(self, event: pygame.event.Event):
        for i in range(self.max_other + self.max_menu):
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.rect[i].collidepoint(event.pos):
                    self.select_menu(i)
                    break  # 한 번에 여러 개의 메뉴가 눌리지 않도록 처리
            elif event.type == pygame.MOUSEMOTION:
                if self.rect[i].collidepoint(event.pos):
                    # highlight 대상을 변경
                    self.highlight = i
                    # 키보드 선택 해제
                    self.selected = -1
            elif event.type == pygame.KEYDOWN:
                if self.pressed == False:
                    self.pressed = True
                    # 엔터 키가 눌렸을 때
                    if event.key == setting.options["enter"]:
                        # 키보드로 선택한 것이 있다면 그 메뉴를 선택
                        if self.selected != -1:
                            self.select_menu(self.selected)
                    elif event.key == setting.options["up"]:
                        # 선택을 하나 위로 이동
                        self.selected = self.selected - 1 if 0 < self.selected else 0
                        self.highlight = self.selected
                    elif event.key == setting.options["down"]:
                        # 선택을 하나 아래로 이동
                        self.selected = (
                            self.selected + 1
                            if self.selected < self.max_other + self.max_menu - 1
                            else self.max_other + self.max_menu - 1
                        )
                        self.highlight = self.selected

            # 버튼이 누르고 있어도 계속 동작하지 않게 뗄 때까지는 작동 방지
            elif event.type == pygame.KEYUP:
                self.pressed = False