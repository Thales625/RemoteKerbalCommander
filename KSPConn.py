import krpc

def debug(text:str):
    print(f"KSPConn> {text}")

class KSPConnection:
    def __init__(self) -> None:
        self.connected = False

        try:
            self.conn = krpc.connect("RKC")
        except ConnectionRefusedError:
            self.connected = False
            debug("Connection refused!")
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