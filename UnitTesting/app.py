import pygame, sys
from queue import Queue
from threading import Thread
from pydotmap import DotMap
import base64
import io

meq = Queue()
api_q = Queue()
buttons = dict()
class Button:
    def __init__(self, id, text, width, height, pos, elevation):
        #Core attributes 
        self.id = id
        self.pressed = False
        self.elevation = elevation
        self.dynamic_elevation = elevation
        self.original_y_pos = pos[1]

        # top rectangle 
        self.top_rect = pygame.Rect(pos, (width, height))
        self.top_color = (71, 95, 119)

        # bottom rectangle 
        self.bottom_rect = pygame.Rect(pos, (width, height))
        self.bottom_color = (53, 75, 94)
        #text
        self.text = text
        self.text_surf = gui_font.render(text, True, (255,255,255))
        self.text_rect = self.text_surf.get_rect(center = self.top_rect.center)
        buttons[id] = self

    def change_text(self, newtext):
        self.text_surf = gui_font.render(newtext, True, (255,255,255))
        self.text_rect = self.text_surf.get_rect(center = self.top_rect.center)

    def draw(self):
        # elevation logic 
        self.top_rect.y = self.original_y_pos - self.dynamic_elevation
        self.text_rect.center = self.top_rect.center

        self.bottom_rect.midtop = self.top_rect.midtop
        self.bottom_rect.height = self.top_rect.height + self.dynamic_elevation

        pygame.draw.rect(screen,self.bottom_color, self.bottom_rect)
        pygame.draw.rect(screen,self.top_color, self.top_rect)
        screen.blit(self.text_surf, self.text_rect)
        self.check_click()

    def check_click(self):
        mouse_pos = pygame.mouse.get_pos()
        if self.top_rect.collidepoint(mouse_pos):
            self.top_color = (215, 75, 75)
            if pygame.mouse.get_pressed()[0]:
                self.dynamic_elevation = 0
                self.pressed = True
                self.change_text(f"{self.text}")
            else:
                self.dynamic_elevation = self.elevation
                if self.pressed == True:
                    meq.put(DotMap({'ev_type': 'button', 'id': self.id}))
                    self.pressed = False
                    self.change_text(self.text)
        else:
            self.dynamic_elevation = self.elevation
            self.top_color = (71, 95, 119)

pygame.init()
screen = pygame.display.set_mode((500, 500))
pygame.display.set_caption('Pix test')
clock = pygame.time.Clock()
gui_font = pygame.font.Font(None, 30)

button = Button('pay', 'Gen payment', 200, 40, (150, 30), 5)

def buttons_draw():
    for b in buttons.values():
        b.draw()

def api_comm(api_queue, out_queue):
    import requests
    import json
    api_public_key = 'TEST-d5055d5d-afa8-481c-a292-cf4ec3559abb'
    api_access_token = 'TEST-4344359610499121-093019-54cca86b7e798704c7b82921bc915abe-704969337'
    api_url = "https://api.mercadopago.com/v1/payments"
    headers = {
        'Authorization': f'Bearer {api_access_token}',
        'Content-Type': 'application/json',
    }
    curr_id = ''
    while True:
        ev = api_queue.get()
        if ev == 'create':
            print('api create will execute')
            data = {
                "transaction_amount": 5,
                "description": "Pix test",
                "payment_method_id": "pix",
                "payer": {
                    "email": "thimil@alunos.utfpr.edu.br",
                    "first_name": "Thiago",
                    "last_name": "Mildemberger",
                    "identification": {
                        "type": "CPF",
                        "number": "01234567890",
                    },
                },
            }
            response = requests.post(api_url, data=json.dumps(data), headers=headers)
            if response.status_code in [201, 200]:
                json_resp = response.json()
                resp = DotMap(json_resp)
                curr_id = resp.id
                print(json_resp)
                print(curr_id)
                out_queue.put(DotMap({
                    'ev_type': 'api',
                    'req_type': ev,
                    'response': response,
                    'qrcode': resp.point_of_interaction.transaction_data.qr_code_base64 + '',
                }))
        if ev == 'check':
            print('api check will execute')
            response = requests.get(api_url + '/' + str(curr_id), headers=headers)
            if response.status_code in [201, 200]:
                json_resp = response.json()
                resp = DotMap(json_resp)
                print(json_resp)
                print(resp.status)
                out_queue.put(DotMap({
                    'ev_type': 'api',
                    'req_type': ev,
                    'response': response,
                    'status': resp.status + '',
                }))
        if ev == 'close':
            print('api close will execute')
            break

    pass

api_thread = Thread(target=api_comm, args=(api_q, meq))
api_thread.start()

qrcode = ()
qrcode_img = ()
show_qrcode = False
api_finished = False

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            if not api_finished:
                api_q.put('close')

            pygame.quit()
            sys.exit()

    screen.fill((220, 221, 216))
    buttons_draw()

    while not meq.empty():
        ev = meq.get()
        if ev.ev_type == 'button':
            if ev.id == 'pay':
                print('pay button click')
                del buttons['pay']
                # call api
                api_q.put('create')
            elif ev.id == 'check':
                print('check button click')
                #call api
                api_q.put('check')
                pass
            elif ev.id == 'close':
                print('close button click')
                #call api
                if not api_finished:
                    api_q.put('close')
                    api_finished = True
                    del buttons['close']
                pass
        elif ev.ev_type == 'api':
            if ev.req_type == 'create':
                print('api create executed')
                qrcode = base64.b64decode(ev.qrcode)
                mem_file = io.BytesIO(qrcode)
                qrcode_img = pygame.image.load(mem_file)
                qrcode_img = pygame.transform.scale(qrcode_img, (500 - 280, 500 - 280))
                show_qrcode = True
                check_button = Button('check', 'Check payment', 200, 40, (150, 220), 5)

            if ev.req_type == 'check':
                print('api check executed')
                if ev.status == 'pending':
                    del buttons['check']
                    print("payment complete")
                    show_qrcode = False
                    close_button = Button('close', 'Close connection', 200, 40, (150, 30), 5)
            pass

    if show_qrcode:
        screen.blit(qrcode_img, (90, 10))


    pygame.display.update()
    clock.tick(60)