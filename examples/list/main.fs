
let range = (l, u) {
    let n = l
    let result = []
    while n < u {
        result += [n]
        n += 1
    }

    return result
}



class Point {
    new = (x, y) {
        self.x = x
        self.y = y
        return self
    }

    move = (x, y) {
        self.x += x
        self.y += y
    }

    goto = (x, y) {
        self.x = x
        self.y = y
    }
}


class Sprite : Point {
    new = (x, y, image) {
        self.goto(x, y)
        self.set_image(image)
        return self
    }

    set_image = (image) {
        self.image = image
    }

    get_image = () {
        return self.image
    }

    __str__ = () {
        return "<" + str(self.get_image()) + " at x: " + str(self.x) + ", y: " + str(self.y) + ">"
    }
}


let make_sprites = () {
    let sprites = []
    for x in range(0, 500) {
        
        sprites += [
            Sprite().new(x, 0, "@")
        ]

    }
    return sprites
}


let print_sprites = (list) {
    putln("[")
    for s in list {
        putln("\t", s)
    }
    putln("]")
}


print_sprites(
    make_sprites()
)