import pymem
import pymem.process
import re


def get_sig(modename, pattern, extra=0, offset=0, relative=True):
    pm = pymem.Pymem('csgo.exe')
    module = pymem.process.module_from_name(pm.process_handle, modename)
    bytes = pm.read_bytes(module.lpBaseOfDll, module.SizeOfImage)
    match = re.search(pattern, bytes).start()
    out = pm.read_int(module.lpBaseOfDll + match + offset) + extra
    return out - module.lpBaseOfDll if relative else out

#example 
#patterns can be viewed at https://github.com/frk1/hazedumper
#pattern : 8D 34 85 ? ? ? ? 89 15 ? ? ? ? 8B 41 08 8B 48 04 83 F9 FF
dwLocalPlayer = get_sig('client.dll', rb'\x8D\x34\x85....\x89\x15....\x8B\x41\x08\x8B\x48\x04\x83\xF9\xFF', 4, 3, True)
#pattern : 8B 0D ? ? ? ? 8B D6 8B C1 83 CA 02
dwForceJump = get_sig('client.dll', rb'\x8B\x0D....\x8B\xD6\x8B\xC1\x83\xCa\x02', 0, 2, True)
#pattern : A1 ? ? ? ? 33 D2 6A 00 6A 00 33 C9 89 B0
dwClientState = get_sig('engine.dll', rb'\xA1....\x33\xD2\x6A\x00\x6A\x00\x33\xC9\x89\xB0', 0, 1, True)

print(f"dwLocalPlayer offset : {dwLocalPlayer}")	
print(f"dwForceJump offset : {dwForceJump}")
print(f"dwClientState offset : {dwClientState}")

input()