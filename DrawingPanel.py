import tkinter as tk
import time


class Color:
    BLACK = "black"
    WHITE = "white"
    RED = "red"
    GREEN = "green"
    BLUE = "blue"
    YELLOW = "yellow"
    ORANGE = "orange"
    PURPLE = "purple"
    PINK = "pink"
    GRAY = "gray"
    GREY = "grey"
    CYAN = "cyan"
    MAGENTA = "magenta"
    BROWN = "brown"
    LIGHT_BLUE = "lightblue"
    LIGHT_GRAY = "lightgray"
    DARK_GRAY = "darkgray"

    def __init__(self, *args):
        self.value = self.to_hex(*args)

    def __str__(self):
        return self.value

    @staticmethod
    def is_rgb(color):
        return (
            isinstance(color, (tuple, list))
            and len(color) == 3
            and all(isinstance(v, (int, float)) and 0 <= v <= 255 for v in color)
        )

    @staticmethod
    def is_hex(color):
        if not isinstance(color, str) or len(color) not in (4, 7) or not color.startswith("#"):
            return False
        try:
            int(color[1:], 16)
            return True
        except ValueError:
            return False

    @staticmethod
    def is_name(color):
        if not isinstance(color, str) or not color:
            return False
        try:
            tk._tkinter.colorstr(color)
            return True
        except Exception:
            return False

    @staticmethod
    def is_valid_color(color):
        return isinstance(color, Color) or Color.is_rgb(color) or Color.is_hex(color) or Color.is_name(color)

    @staticmethod
    def to_rgb(*args):
        if len(args) == 1:
            c = args[0]
            if isinstance(c, Color):
                c = str(c)
            if Color.is_rgb(c):
                return tuple(int(v) for v in c)
            from tkinter import Tk
            root = Tk()
            root.withdraw()
            r, g, b = root.winfo_rgb(c)
            root.destroy()
            return (r//256, g//256, b//256)
        if len(args) == 3:
            return tuple(int(v) for v in args)
        raise ValueError("invalid color")

    @staticmethod
    def to_hex(*args):
        r, g, b = Color.to_rgb(*args)
        return f"#{r:02x}{g:02x}{b:02x}"

    @staticmethod
    def to_name(*args):
        return Color.to_hex(*args)

    @staticmethod
    def normalize_all_colors(options):
        for key in ("color", "fill", "outline"):
            if key in options and options[key] not in ("", None):
                options[key] = Color.to_hex(options[key])


class DrawingPanel:
    def __init__(self, width=500, height=500, background="white", auto_show=True, **options):
        self._width = int(width)
        self._height = int(height)
        self._background = background
        self._outline = "black"
        self._fill = "black"
        self._stroke = 1
        self._title = "DrawingPanel"
        self._visible = True
        self._x = 0
        self._y = 0
        self._mouse_x = 0
        self._mouse_y = 0
        self._auto_show = auto_show

        self.root = tk.Tk()
        self.root.title(self._title)
        self.canvas = tk.Canvas(self.root, width=self._width, height=self._height, bg=background)
        self.canvas.pack()

    def show(self):
        self.root.mainloop()
        return self

    def display(self):
        return self.show()

    def close(self):
        self._visible = False
        self.root.destroy()

    def is_visible(self):
        return self._visible

    @staticmethod
    def is_headless():
        return False

    def clear(self):
        self.canvas.delete("all")
        self.canvas.config(bg=self._background)

    def draw_line(self, x1, y1, x2, y2, color="", **options):
        c = options.get("fill", color or self._outline)
        w = options.get("width", self._stroke)
        self.canvas.create_line(x1, y1, x2, y2, fill=c, width=w)

    def draw_rect(self, x, y, w, h, color="", **options):
        outline = options.get("outline", color or self._outline)
        fill = options.get("fill", None)
        wline = options.get("width", self._stroke)
        self.canvas.create_rectangle(x, y, x+w, y+h, outline=outline, fill=fill, width=wline)

    def draw_rectangle(self, x, y, w, h, color="", **options):
        self.draw_rect(x, y, w, h, color,** options)

    def fill_rect(self, x, y, w, h, color="", **options):
        fill = options.get("fill", color or self._fill)
        outline = options.get("outline", fill)
        wline = options.get("width", self._stroke)
        self.canvas.create_rectangle(x, y, x+w, y+h, fill=fill, outline=outline, width=wline)

    def fill_rectangle(self, x, y, w, h, fill="", color="", **options):
        chosen = fill if fill not in ("", None) else color
        self.fill_rect(x, y, w, h, chosen,** options)

    def draw_oval(self, x, y, w, h, color="", **options):
        outline = options.get("outline", color or self._outline)
        fill = options.get("fill", None)
        wline = options.get("width", self._stroke)
        self.canvas.create_oval(x, y, x+w, y+h, outline=outline, fill=fill, width=wline)

    def fill_oval(self, x, y, w, h, color="", **options):
        fill = options.get("fill", color or self._fill)
        outline = options.get("outline", fill)
        wline = options.get("width", self._stroke)
        self.canvas.create_oval(x, y, x+w, y+h, fill=fill, outline=outline, width=wline)

    def draw_pixel(self, x, y, color="", **options):
        c = color or self._outline
        self.canvas.create_rectangle(x, y, x+1, y+1, fill=c, outline=c)

    def draw_polyline(self, *coords, **options):
        raw = list(coords)
        color = self._outline
        if raw and isinstance(raw[-1], str) and Color.is_valid_color(raw[-1]):
            color = raw.pop()
        pts = []
        for i in range(0, len(raw), 2):
            pts.append((raw[i], raw[i+1]))
        if len(pts)>=2:
            w = options.get("width", self._stroke)
            self.canvas.create_line(pts, fill=options.get("fill", color), width=w)

    def draw_polygon(self, *coords, **options):
        raw = list(coords)
        color = self._outline
        if raw and isinstance(raw[-1], str) and Color.is_valid_color(raw[-1]):
            color = raw.pop()
        pts = []
        for i in range(0, len(raw), 2):
            pts.append((raw[i], raw[i+1]))
        if len(pts)>=2:
            fill = options.get("fill", None)
            outline = options.get("outline", color)
            self.canvas.create_polygon(pts, fill=fill, outline=outline)

    def fill_polygon(self, *coords, **options):
        raw = list(coords)
        color = self._fill
        if raw and isinstance(raw[-1], str) and Color.is_valid_color(raw[-1]):
            color = raw.pop()
        pts = []
        for i in range(0, len(raw), 2):
            pts.append((raw[i], raw[i+1]))
        if len(pts)>=2:
            fill = options.get("fill", color)
            outline = options.get("outline", fill)
            self.canvas.create_polygon(pts, fill=fill, outline=outline)

    def draw_arc(self, x, y, w, h, start_angle, extent, color="", **options):
        c = options.get("outline", color or self._outline)
        wline = options.get("width", self._stroke)
        self.canvas.create_arc(x, y, x+w, y+h, start=start_angle, extent=extent, style=tk.ARC, outline=c, width=wline)

    def fill_arc(self, x, y, w, h, start_angle, extent, color="", **options):
        fill = options.get("fill", color or self._fill)
        outline = options.get("outline", fill)
        self.canvas.create_arc(x, y, x+w, y+h, start=start_angle, extent=extent, style=tk.PIESLICE, fill=fill, outline=outline)

    def draw_string(self, text, x, y, color="", font="", **options):
        c = options.get("fill", color or self._outline)
        self.canvas.create_text(x, y, text=str(text), fill=c, anchor="nw")

    def draw_image(self, filename, x=0, y=0, w=0, h=0, **options):
        # Tk图片简化实现，大图片复杂，基础可用
        from PIL import Image, ImageTk
        img = Image.open(filename).convert("RGB")
        if w>0 and h>0:
            img = img.resize((int(w), int(h)))
        self._tk_img = ImageTk.PhotoImage(img)
        self.canvas.create_image(x, y, image=self._tk_img, anchor="nw")

    def save(self, filename):
        # 截图保存，需要pillow
        from PIL import ImageGrab
        x = self.root.winfo_rootx() + self.canvas.winfo_x()
        y = self.root.winfo_rooty() + self.canvas.winfo_y()
        x1 = x + self.canvas.winfo_width()
        y1 = y + self.canvas.winfo_height()
        ImageGrab.grab().crop((x,y,x1,y1)).save(filename)

    def save_as(self, filename):
        self.save(filename)

    def get_pixel_color_rgb(self, x, y):
        # tk原生不支持读像素，用截图读取
        from PIL import ImageGrab
        x0 = self.root.winfo_rootx() + self.canvas.winfo_x() + x
        y0 = self.root.winfo_rooty() + self.canvas.winfo_y() + y
        img = ImageGrab.grab()
        return img.getpixel((x0,y0))

    def get_pixel(self, x, y):
        return self.get_pixel_color_rgb(x, y)

    def get_pixel_color(self, x, y):
        r,g,b = self.get_pixel_color_rgb(x,y)
        return f"#{r:02x}{g:02x}{b:02x}"

    def get_width(self):
        return self._width
    def get_height(self):
        return self._height
    def get_size(self):
        return (self._width, self._height)

    def set_size(self, width, height):
        self._width, self._height = int(width), int(height)
        self.canvas.config(width=self._width, height=self._height)

    def set_width(self, width):
        self.set_size(width, self._height)
    def set_height(self, height):
        self.set_size(self._width, height)

    def get_background(self):
        return self._background
    def set_background(self, color):
        self._background = color
        self.canvas.config(bg=color)

    def get_color(self):
        return self._outline
    def set_color(self, color):
        self._outline = color

    def get_fill_color(self):
        return self._fill
    def set_fill_color(self, color):
        self._fill = color

    def get_stroke(self):
        return self._stroke
    def get_stroke_width(self):
        return self._stroke
    def set_stroke(self, w):
        self._stroke = int(w)
    def set_stroke_width(self, w):
        self.set_stroke(w)

    def get_title(self):
        return self._title
    def set_title(self, title):
        self._title = str(title)
        self.root.title(self._title)

    def sleep(self, ms):
        time.sleep(ms / 1000.0)
        self.root.update()

    def animate(self, delay, func):
        while self._visible:
            self.sleep(delay)
            func()
            self.root.update()

    def center(self):
        self.root.update_idletasks()
        w = self.root.winfo_width()
        h = self.root.winfo_height()
        sw = self.root.winfo_screenwidth()
        sh = self.root.winfo_screenheight()
        x = (sw - w)//2
        y = (sh - h)//2
        self.root.geometry(f"{w}x{h}+{x}+{y}")

    def set_location(self, x, y):
        self.root.geometry(f"+{x}+{y}")
    def get_location(self):
        return (self._x, self._y)

    def set_visible(self, visible):
        self._visible = bool(visible)
        if self._visible:
            self.show()
        else:
            self.root.withdraw()

    def message(self, text, title=""):
        tk.messagebox.showinfo(title, text)

    def add_key_listener(self, function, event_type="press"):
        self.root.bind("<Key>", lambda e: function(e))

    def add_mouse_listener(self, function, event_type="click"):
        self.canvas.bind("<Button-1>", lambda e: function(e))
