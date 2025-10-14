from PyQt6.QtWidgets import QWidget

class Router:
    def navigate(self, current: QWidget, screen_cls, *args, **kwargs):
        next_screen = screen_cls(*args, **kwargs)
        next_screen.show()
        if current is not None:
            try:
                current.close()
            except Exception:
                pass
        return next_screen

router = Router()
