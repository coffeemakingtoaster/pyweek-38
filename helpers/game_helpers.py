from panda3d.core import WindowProperties

def lock_mouse_in_window():
    props = WindowProperties()
    props.setMouseMode(WindowProperties.M_confined)
    base.win.requestProperties(props)


def release_mouse_from_window():
    props = WindowProperties()
    props.setMouseMode(WindowProperties.M_absolute)
    base.win.requestProperties(props)

