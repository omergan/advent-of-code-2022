from dataclasses import dataclass
from pathlib import Path
input_file = Path('input.txt').read_text()
commands = input_file.split('\n')

strengths = []
W = 40
OPCODE_CYCLES = dict(noop=1, addx=2)

@dataclass
class Instruction:
    opcode: str
    value: int

class Device:
    register = 1
    cycle_n = 1
    reg_history = [] # Indexed by cycle
    signal_breakpoints = [20,60,100,140,180,220]

    def execute(self, inst: Instruction):
        cycles_to_run = OPCODE_CYCLES[inst.opcode]
        for cycle in range(cycles_to_run):
            if self.cycle_n in self.signal_breakpoints:
                strengths.append(self.cycle_n * self.register)
            self.reg_history.append(self.register)
            self.cycle_n += 1
            self.register += inst.value if cycle == cycles_to_run - 1 else 0

    @property
    def display(self) -> str:
        crt = ""
        for i, p in enumerate(self.reg_history):
            crt += "#" if  abs(i % W - p) <= 1 else " "
            crt += "\n" if i % W == W - 1 else ""
        return crt

def simulate(device: Device, commands: list) -> None:
    for c in commands:
        args = tuple(c.split(" "))
        val = int(args[1]) if len(args) > 1 else 0

        inst = Instruction(opcode=args[0], value=val)
        device.execute(inst)

if __name__ == '__main__':
    device = Device()
    simulate(device, commands)
    print(strengths)
    print(device.display)
