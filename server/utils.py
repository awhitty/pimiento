def do_rgb(r,g,b):
    r /= 255
    g /= 255
    b /= 255

    red.ChangeDutyCycle(r*100)
    green.ChangeDutyCycle(g*100)
    blue.ChangeDutyCycle(b*100)

def handle_update(snapshot):
    data = snapshot.val()

    r = data['red']['value']
    g = data['green']['value']
    b = data['blue']['value']

    do_rgb(r,g,b)