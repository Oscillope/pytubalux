from buttons import Buttons

config_tree = {
    "mode": ["leader", "member", "self"],
    "ssid": ["netnet", "trombonet", "saxotubes", "tubanet"],
}

button_mode = "selector"

def menu_timeout(timer):
    global button_mode
    screen.drawtext()
    screen.softbtn(["Down", "Enter"])
    button_mode = "selector"

def softkey_enter():
    screen.menu(config_tree[screen.menu_str], 0)

def softkey_up():
    try:
        screen.menu_pos -= 1
    except ValueError:
        pass
    menu_timer.init(period=2000, mode=machine.Timer.ONE_SHOT, callback=menu_timeout)

def softkey_down():
    try:
        screen.menu_pos += 1
    except ValueError:
        pass
    menu_timer.init(period=2000, mode=machine.Timer.ONE_SHOT, callback=menu_timeout)

button_callbacks = {
    "selector": (softkey_down, softkey_enter),
    "up/down": (softkey_up, softkey_down),
}

def conf1_cb():
    try:
        button_callbacks[button_mode][0]()
    except KeyError:
        screen.print("OOPS " + button_mode)

def conf2_cb():
    try:
        button_callbacks[button_mode][1]()
    except KeyError:
        screen.print("OOPS " + button_mode)


btns = Buttons([(12, conf1_cb), (14, conf2_cb)])

def enter_config(screen, timer):
    pass
