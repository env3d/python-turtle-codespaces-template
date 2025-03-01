# type: ignore

import importlib.util

module_path = "/usr/local/lib/python3.9/turtle.py"  # Full path to the module
module_name = "turtle"

spec = importlib.util.spec_from_file_location(module_name, module_path)
# print(spec)
mymodule = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mymodule)
# print(dir(mymodule))

globals().update({name: getattr(mymodule, name) for name in dir(mymodule) if not name.startswith("_")})

# Turtle = mymodule.Turtle

def Screen():
    import setup
    _s = mymodule.Screen()
    _s.exitonclick = lambda : None
    _s.screensize(canvwidth=setup.SCREEN_WIDTH, canvheight=setup.SCREEN_HEIGHT)
    _s.setup(setup.SCREEN_WIDTH+20,setup.SCREEN_HEIGHT+20)
    return _s


 