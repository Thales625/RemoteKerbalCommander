from json import dumps as Stringify

def debug(text:str):
    print(f"Conn Manager> {text}")

def format_value(field):
    return f"{field:.2f}" if isinstance(field, float) else str(field)

class Module:
    def __init__(self, name, data, setup, render, on_error=lambda: None, running=lambda: None) -> None:
        self.name = name
        self.data = data
        self.setup = setup
        self.render = render
        self.on_error = on_error
        self.running = running

class ConnectionManager:
    def __init__(self, emit_func, ksp_conn, cam_conn) -> None:
        self.emit_func = emit_func

        self.modules = []

        self.add_module(
            Module(
                "params",
                {
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
                lambda data: {block: [field for field in data[block]] for block in data},
                lambda data: [self.emit_func(f"update.params:{block}", Stringify([format_value(data[block][field]()) for field in data[block]]).replace(" ", "")) for block in data],
                lambda reason: (self.emit_func("module-error", "KSP Communication failed!"), setattr(ksp_conn, "connected", False)),
                lambda: ksp_conn.connected
            )   
        )


        self.add_module(
            Module(
                "camera",
                { cam.id: cam.get_image for cam in cam_conn.cameras },
                lambda data: {cam: {} for cam in data},
                lambda data: [self.emit_func(f"update.camera:{cam}", data[cam]()) for cam in data],
                lambda reason: (self.emit_func("module-error", "Camera Communication failed!"), setattr(cam_conn, "connected", False)),
                lambda: cam_conn.connected
            )
        )


    def add_module(self, module):
        self.modules.append(module)

    def emit_values(self):
        for module in self.modules:
            if module.running():
                try:
                    module.render(module.data)
                except Exception as e:
                    module.on_error(e)

                    debug(f"Module {module.name} Error!")

    def emit_setup(self):
        self.emit_func("setup", Stringify({m.name: m.setup(m.data) for m in self.modules}).replace(", ", ",").replace(": ", ":"))