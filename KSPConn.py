import krpc
from time import time
from json import dumps as Stringify

def round_list(array):
    return list(map(lambda x: f"{x:.2f}" if isinstance(x, float) else str(x), array))


'''
on_connected: send setup to client
'''

class KSPConnection:
    def __init__(self) -> None:
        self.connected = False

        try:
            self.conn = krpc.connect("RKC")
        except ConnectionRefusedError:
            print("kRPC > Connection refused!")
            return
        
        self.connected = True
        
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
                        "eccentricity":self.conn.add_stream(getattr, self.orbit, "eccentricity")
                    },
                    "resource": {
                        "battery": lambda: (self.stream_resources().amount("ElectricCharge") / self.stream_resources().max("ElectricCharge")) * 100,
                        "fuel": lambda: (self.stream_resources().amount("LiquidFuel") / self.stream_resources().max("LiquidFuel")) * 100
                    }
                },
                "setup": lambda data: {block: [field for field in data[block]] for block in data},
                "render": lambda data: [[(lambda value: f"{value:.2f}" if isinstance(value, float) else str(value))(data[block][field]()) for field in data[block]] for block in data], # <----------- ESQUIZOFRENIA!!!!!!!!
                #"render": lambda data: {block: {field: (lambda value: f"{value:.2f}" if isinstance(value, float) else str(value))(data[block][field]()) for field in data[block]} for block in data}, # <----------- ESQUIZOFRENIA!!!!!!!!
            },

            "camera": {
                "data": {
                    "19239812": {
                        
                    }
                },
                "setup": lambda x: x,
                "render": lambda x: [i for i in x]
            },
        }

        self.setup_message = Stringify({m:n["setup"](n["data"]) for m, n in self.modules.items()}).replace(", ", ",").replace(": ", ":")
        
        self.get_values = lambda: Stringify({m:n["render"](n["data"]) for m, n in self.modules.items()}).replace(", ", ",").replace(": ", ":")





    def format_message(self, data:object):
        return Stringify(
            {
                "send_at": 1000 * time(),
                "data": data
            }
        )


