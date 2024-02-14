import krpc
from json import dumps as Stringify
from time import time

def debug(text:str):
    print(f"KSPConn> {text}")

def format_value(field):
    return f"{field:.2f}" if isinstance(field, float) else str(field)

class KSPConnection:
    def __init__(self, cameras) -> None:
        self.on_error = lambda reason: None

        self.connected = False

        try:
            self.conn = krpc.connect("RKC")
        except ConnectionRefusedError:
            debug("Connection refused!")
            return
        
        self.connected = True

        self.cameras = [{"id": cam.id, "get_image": cam.get_image} for cam in cameras]
        
        self.space_center = self.conn.space_center
        self.vessel = self.space_center.active_vessel
        self.orbit = self.vessel.orbit
        self.body = self.orbit.body

        self.body_ref = self.body.reference_frame
        self.surface_ref = self.vessel.surface_reference_frame
        self.flight_body = self.vessel.flight(self.body_ref)
        self.flight_surf = self.vessel.flight(self.surface_ref)
        
        self.stream_situation = self.conn.add_stream(getattr, self.vessel, "situation")
        self.stream_resources = self.conn.add_stream(getattr, self.vessel, "resources")

        self.modules = {
            "params": {
                "data": {
                    "flight": {
                        "ut": self.conn.add_stream(getattr, self.space_center, "ut"),
                        "situation": lambda: self.stream_situation().name,
                        "mass": self.conn.add_stream(getattr, self.vessel, "mass"),
                        "alt": self.conn.add_stream(getattr, self.flight_body, "surface_altitude"),
                        "vel": self.conn.add_stream(getattr, self.flight_body, "speed"),
                        "pitch": self.conn.add_stream(getattr, self.flight_surf, "pitch")
                    },
                    "orbit": {
                        "name": self.conn.add_stream(getattr, self.body, "name"),
                        "apoapsis": self.conn.add_stream(getattr, self.orbit, "apoapsis_altitude"),
                        "periapsis": self.conn.add_stream(getattr, self.orbit, "periapsis_altitude"),
                        "inclination": self.conn.add_stream(getattr, self.orbit, "inclination"),
                        "eccentricity": self.conn.add_stream(getattr, self.orbit, "eccentricity")
                    },
                    "resource": {
                        "battery": lambda: f"{((self.stream_resources().amount('ElectricCharge') / self.stream_resources().max('ElectricCharge')) * 100):.2f}%",
                        "fuel": lambda: f"{((self.stream_resources().amount('LiquidFuel') / self.stream_resources().max('LiquidFuel')) * 100):.2f}%"
                    }
                },
                "setup": lambda data: {block: [field for field in data[block]] for block in data},
                "render": lambda data, emit_func: [emit_func(f"update.params:{block}", Stringify([format_value(data[block][field]()) for field in data[block]]).replace(" ", "")) for block in data],
            },

            "camera": {
                "data": {cam["id"]: cam["get_image"] for cam in self.cameras},
                "setup": lambda data: {cam: {} for cam in data},
                "render": lambda data, emit_func: [emit_func(f"update.camera:{cam}", data[cam]()) for cam in data]
            },
        }

    def emit_values(self, emit_func):
        try:
            for m, n in self.modules.items():
                n["render"](n["data"], emit_func)
        except ZeroDivisionError:
            self.connected = False

            self.on_error("KSPConnection failed!")

            debug("Lost connection!")

    def emit_setup(self, emit_func):
        emit_func("setup", Stringify({m: n["setup"](n["data"]) for m, n in self.modules.items()}).replace(", ", ",").replace(": ", ":"))