import rpyc
import time
from rich.live import Live
from rich.table import Table
import yaml 
with open('joystick_config.yaml', 'r') as file:
    my_dict = yaml.safe_load(file)

values = [value for _, value in my_dict['joystick'].items()]

conn = rpyc.connect("localhost", 18861)

def generate_table() -> Table:
    """Make a new table."""
    table = Table()
    table.add_column("Time")
    table.add_column("Key")
    table.add_column("Value")
    now = str(time.strftime("%H:%M:%S", time.localtime()))
    data = conn.root.getJoystickStatus()

    for i in values:
        table.add_row(f"{now}", f"{i}", f"{round(data[i],3)}")

    return table



with Live(generate_table(), refresh_per_second=1000) as live:
    while True:
        live.update(generate_table())
