from json import dumps as Stringify
from json import loads as Parse

def debug(text:str):
    print(f"Conn Manager> {text}")

def format_value(field):
    return f"{field:.2f}" if isinstance(field, float) else str(field)

class Module:
    def __init__(self, name, data, setup, send, running, recv_setup=None, on_error=None) -> None:
        self.name = name
        self.data = data
        self.setup = setup
        self.send = send
        self.running = running
        self.recv_setup = recv_setup
        self.on_error = on_error

class ConnectionManager:
    def __init__(self, emit_func, add_route_func, ksp_conn, cam_conn) -> None:
        self.emit_func = emit_func
        self.add_route_func = add_route_func

        self.modules = []


        def send_params(data):
            #lambda data: [self.emit_func(f"update.params:{block}", Stringify([format_value(data[block][field]()) for field in data[block]]).replace(" ", "")) for block in data],

            for field in data:
                msg = Stringify([format_value(data[field][attr]()) for attr in data[field]]).replace(" ", "")
                self.emit_func(f"update.params:{field}", msg)

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
                send=send_params,
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





        def recv_setup_controller(module):
            for field in module.data:
                for attr in module.data[field]:
                    on_recv = lambda value, field=field, attr=attr: (module.data[field][attr][0](value), self.emit_func(f"update:controller:{field}:{attr}", value) if module.running() else None)

                    self.add_route_func(f"update:{module.name}:{field}:{attr}")(on_recv)
                    
        self.add_module(
            Module(
                name="controller",
                data={
                    "slider": { # field
                        "throttle": ( # attribute
                            lambda value: setattr(ksp_conn.vessel.control, "throttle", float(value) * 1e-2),
                            (0, 100),
                            lambda: f"{(getattr(ksp_conn.vessel.control, 'throttle') * 1e2):.2f}"
                        )
                    },
                    "switch": {
                        "lights": (
                            lambda value: setattr(ksp_conn.vessel.control, "lights", bool(value)),
                            (0, 1),
                            lambda: getattr(ksp_conn.vessel.control, "lights")
                        ),
                        "gears": (
                            lambda value: setattr(ksp_conn.vessel.control, "gear", bool(value)),
                            (0, 1),
                            lambda: getattr(ksp_conn.vessel.control, "gear")
                        ),
                        "brakes": (
                            lambda value: setattr(ksp_conn.vessel.control, "brakes", bool(value)),
                            (0, 1),
                            lambda: getattr(ksp_conn.vessel.control, "brakes")
                        )
                    }
                },
                setup=lambda data: {field: {attr:{"interval": data[field][attr][1], "value": data[field][attr][2]()} for attr in data[field]} for field in data},
                send=None,
                on_error=lambda reason: (self.emit_func("module-error", "KSP Communication failed!"), setattr(ksp_conn, "connected", False)),
                recv_setup=recv_setup_controller,
                running=lambda: ksp_conn.connected
            )   
        )

    def add_module(self, module):
        # add recv route
        if module.recv_setup:
            try:
                module.recv_setup(module)
            except Exception as e:
                module.on_error(e)
                debug(f"Moudle: {module.name} error")
            
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
        self.emit_func("setup", Stringify({m.name: m.setup(m.data) for m in self.modules}))