import os
import sys
from dataclasses import dataclass, field

@dataclass
class Ping:

    uid: int
    filename: str
    ping_number: int
    timestamp: float
    proj: str
    x_coord: float
    y_coord: float
    assigned_svp: str