# server.py
import rpyc
import yaml


with open('joystick_config.yaml', 'r') as file:
    my_dict = yaml.safe_load(file)

values = [value for _, value in my_dict['joystick'].items()]

class MyService(rpyc.Service):
    joystickStatus: dict = dict()
    object_count = 0
    instruction = ""

    def __init__(self) -> None:
        super().__init__()
        for i in values:
            self.joystickStatus[i] = 0
    
    def exposed_setter(self, object_count_arg, instruction_arg):
        self.object_count = object_count_arg
        self.instruction = instruction_arg

    def exposed_getter(self):
        return [self.object_count, self.instruction]
    
    def exposed_setJoystickStatus(self, key, value):
        self.joystickStatus[key] = value

    def exposed_getJoystickStatus(self):
        return self.joystickStatus


service = MyService()

if __name__ == "__main__":
    from rpyc.utils.server import ThreadedServer
    t = ThreadedServer(service, port=18861)
    t.start()