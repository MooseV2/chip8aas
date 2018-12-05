# chip8aas

A simple guide to running this application:

1. Install the requirements with `pip install -r requirements.txt`
2. Start the registry with `python Utils/registry.py`
3. Start one or more worker nodes (may be run on different devices) with `python worker.py`
4. Launch a CHIP-8 ROM file using the command `python main.py <rom file>`. Some ROMs can be found in the ROMS directory. For example, `python main.py ROMS/MAZE`

A web browser window with the display should appear.
