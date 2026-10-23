import subprocess
from pathlib import Path


class RunEnergyPlusToFMU:
    def __init__(
        self,
        idf="_fmu-export-variable.idf",
        epw="USA.epw",
        directory="/home/fmu/code/energy/test",
    ):
        self.idf = Path(idf)
        self.epw = Path(epw)
        self.directory = Path(directory)

    def run(self):
        self.directory.mkdir(parents=True, exist_ok=True)
        command = [
            "python",
            "/home/fmu/code/energy/Scripts/EnergyPlusToFMU.py",
            "-d",
            "-i",
            "/home/fmu/code/Energy+.idd",
            "-w",
            str(self.epw),
            str(self.idf),
        ]
        subprocess.run(command, cwd=self.directory, check=True)
        return "success"

