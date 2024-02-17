from json import dumps as Stringify
from json import loads as Parse

def debug(text:str):
    print(f"Conn Manager> {text}")

def format_value(field):
    return f"{field:.2f}" if isinstance(field, float) else str(field)

class Module:
    def __init__(self, name, data, setup, send, running, on_recv=None, on_error=None) -> None:
        self.name = name
        self.data = data
        self.setup = setup
        self.send = send
        self.running = running
        self.on_recv = on_recv
        self.on_error = on_error

class ConnectionManager:
    def __init__(self, emit_func, add_route_func, ksp_conn, cam_conn) -> None:
        self.emit_func = emit_func
        self.add_route_func = add_route_func

        self.modules = []

        self.add_module(
            Module(
                name="params",
                data={
                    "flight": {
                        "ut": ksp_conn.conn.add_stream(getattr, ksp_conn.space_center, "ut"),
                        "situation": lambda: ksp_conn.stream_situation().name,
                        "mass": ksp_conn.conn.add_stream(getattr, ksp_conn.vessel, "mass"),
                        "alt": ksp_conn.conn.add_stream(getattr, ksp_conn.flight_body, "surface_altitude"),
                        "vel": ksp_conn.conn.add_stream(getattr, ksp_conn.flight_body, "speed"),
                        "pitch": ksp_conn.conn.add_stream(getattr, ksp_conn.flight_surf, "pitch")
                    },
                    "orbit": {
                        "name": ksp_conn.conn.add_stream(getattr, ksp_conn.body, "name"),
                        "apoapsis": ksp_conn.conn.add_stream(getattr, ksp_conn.orbit, "apoapsis_altitude"),
                        "periapsis": ksp_conn.conn.add_stream(getattr, ksp_conn.orbit, "periapsis_altitude"),
                        "inclination": ksp_conn.conn.add_stream(getattr, ksp_conn.orbit, "inclination"),
                        "eccentricity": ksp_conn.conn.add_stream(getattr, ksp_conn.orbit, "eccentricity")
                    },
                    "resource": {
                        "battery": lambda: f"{((ksp_conn.stream_resources().amount('ElectricCharge') / ksp_conn.stream_resources().max('ElectricCharge')) * 100):.2f}%",
                        "fuel": lambda: f"{((ksp_conn.stream_resources().amount('LiquidFuel') / ksp_conn.stream_resources().max('LiquidFuel')) * 100):.2f}%"
                    },
                },
                setup=lambda data: {block: [field for field in data[block]] for block in data},
                send=lambda data: [self.emit_func(f"update.params:{block}", Stringify([format_value(data[block][field]()) for field in data[block]]).replace(" ", "")) for block in data],
                on_error=lambda reason: (self.emit_func("module-error", "KSP Communication failed!"), setattr(ksp_conn, "connected", False)),
                running=lambda: ksp_conn.connected
            )   
        )


        self.add_module(
            Module(
                name="camera",
                data={ cam.id: cam.get_image for cam in cam_conn.cameras },
                setup=lambda data: {cam: {} for cam in data},
                send=lambda data: [self.emit_func(f"update.camera:{cam}", data[cam]()) for cam in data],
                on_error=lambda reason: (self.emit_func("module-error", "Camera Communication failed!"), setattr(cam_conn, "connected", False)),
                running=lambda: cam_conn.connected
            )
        )

        self.add_module(
            Module(
                name="controller",
                data={
                    "slider": {
                        "throttle": lambda value: setattr(ksp_conn.vessel.control, "throttle", value),
                    }
                },
                setup=lambda data: {block: [field for field in data[block]] for block in data},
                send=None,
                on_error=lambda reason: (self.emit_func("module-error", "KSP Communication failed!"), setattr(ksp_conn, "connected", False)),
                on_recv=lambda field, msg: (lambda obj: [field[f](obj[f]) for f in obj])(Parse(msg)),
                running=lambda: ksp_conn.connected
            )   
        )



    def add_module(self, module):
        if module.on_recv:
            for field in module.data:
                self.add_route_func(f"update:{module.name}:{field}")(lambda msg: module.on_recv(module.data[field], msg))

        self.modules.append(module)

    def emit_values(self):
        for module in self.modules:
            if module.send and module.running():
                try:
                    module.send(module.data)
                except Exception as e:
                    module.on_error(e)

                    debug(f"Module {module.name} Error!")

    def emit_setup(self):
        self.emit_func("setup", Stringify({m.name: m.setup(m.data) for m in self.modules}).replace(", ", ",").replace(": ", ":"))