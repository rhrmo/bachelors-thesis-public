import subprocess
import pynvml
import time
import output
import os
import psutil


class Hashcat:
    config: dict

    def __init__(self, config, hsPath, outputPath):
        self.config = config
        self.hsPath = hsPath
        self.outputPath = outputPath
    
    # run dummy test to heat up the GPU
    def dummy(self):
        args = []
        args.append(self.hsPath)
        args.append("-a")
        args.append("3")
        args.append("-m")
        args.append("1700")
        args.append("e5c3ede3e49fb86592fb03f471c35ba13e8d89b8ab65142c9a8fdafb635fa2223c24e5558fd9313e8995019dcbec1fb584146b7bb12685c7765fc8c0d51379fd")
        args.append("--runtime=5")
        subprocess.run(args, stdin = subprocess.PIPE, stdout=subprocess.PIPE, stderr = subprocess.PIPE, universal_newlines=True)

    # run hashcat in benchmark mode
    def benchmark(self, folder, gpuName):
        args = []
        args.append(self.hsPath)
        args.append("-b")
        args.append("--machine-readable")
        args.append("--quiet")
        process = subprocess.run(args, stdin = subprocess.PIPE, stdout=subprocess.PIPE, stderr = subprocess.PIPE, universal_newlines=True)
        output.saveBM(process.stdout, process.stderr, folder, gpuName)

    # return the name of the GPU that is currently in the system
    def getGpuName(self):
        info = self.getGpuInfo()
        if info.stderr != "":
            print("getGpuInfo() error:")
            print(info.stderr)
        stdOut = info.stdout
        namePos = stdOut.find("Name")
        name = stdOut[namePos+17:] # 17 characters after N in Name is beginning of the name of the GPU
        return name[:name.find("\n")]

    # return the output of hashcat -I
    def getGpuInfo(self):
        args = [self.hsPath, "-I"]
        return subprocess.run(args, stdin = subprocess.PIPE, stdout=subprocess.PIPE, stderr = subprocess.PIPE, universal_newlines=True)

    # run the hashcat application and save the output after it is done running
    def runHashcat(self, hash, hashfiles, potfile, inputName, memory_dataFolder, amd):
        if hashfiles != "":
            hash[2] = os.path.join(hashfiles, hash[2]) 
        args = [self.hsPath]
        args += setAttributes(self, hash)
        args.append("--machine-readable")
        args.append("--status")
        args.append("--status-timer=1")
        args.append("--quiet")
        t = time.localtime()
        current_time = time.strftime("%H:%M:%S", t)
        print(current_time)
        print(args)
        if (os.path.isfile(potfile) == True):
            os.remove(potfile)

        mem_total = []
        mem_used = []
        mem_util = []
        bus_util = []
        try:
            process = subprocess.Popen(args, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
            start_time = time.time()
            while True:  # While the process is running
                return_code = process.poll()
                if return_code is not None:  # Process has completed
                    break
                
                elapsed_time = time.time() - start_time
                if elapsed_time >= 80:
                    process.kill()
                    print("hashcat.run ERROR: TimeoutExpired")
                    return
                if amd == False:
                    gpu_mem_util = get_nvidia_gpu_memory_utilization()
                    gpu_bus_util = get_nvidia_gpu_bus_utilization()
                    mem_total.append(gpu_mem_util[0])
                    mem_used.append(gpu_mem_util[1])
                    mem_util.append(gpu_mem_util[2])
                    bus_util.append(gpu_bus_util[0])
                else:
                    total_memory, used_memory, memory_utilization = get_amd_gpu_memory_utilization()
                    mem_total.append(total_memory)
                    mem_used.append(used_memory)
                    mem_util.append(memory_utilization)
                    bus_util.append(None)
                time.sleep(1)

            stdout, stderr = process.communicate(timeout=80)
        except subprocess.TimeoutExpired:
            process.kill()
            stdout, stderr = process.communicate()
            print("hashcat.run ERROR: TimeoutExpired")
            return
        except Exception as e:
            print("hashcat.run ERROR:", e)
            return

        output.saveOutput(stdout, stderr, os.path.join(self.outputPath, os.path.splitext(inputName)[0] + "-" + fixHashName(hash[1])), 
                          args, mem_total, mem_used, mem_util, bus_util, os.path.join(memory_dataFolder, os.path.splitext(inputName)[0] + "-" + fixHashName(hash[1])))

# return memory utilisation values for nvidia gpu
def get_nvidia_gpu_memory_utilization():
    pynvml.nvmlInit()
    
    handle = pynvml.nvmlDeviceGetHandleByIndex(0)
    mem_info = pynvml.nvmlDeviceGetMemoryInfo(handle)
    total_memory = mem_info.total / 1024 / 1024  # Convert bytes to MB
    used_memory = mem_info.used / 1024 / 1024   # Convert bytes to MB
    memory_utilization = used_memory / total_memory * 100

    pynvml.nvmlShutdown()
    return total_memory, used_memory, memory_utilization

# return bus utilisation value for nvidia gpu
def get_nvidia_gpu_bus_utilization():
    gpu_bus_utilization = []
    try:
        output = subprocess.check_output(["nvidia-smi", "--query-gpu=utilization.gpu", "--format=csv,nounits"], universal_newlines=True)
        lines = output.strip().split("\n")[1:]  # Skip the header line

        for line in lines:
            bus_utilization = float(line)
            gpu_bus_utilization.append(bus_utilization)

    except subprocess.CalledProcessError as e:
        print("Error while fetching NVIDIA GPU bus utilization:", e)
        gpu_bus_utilization = []

    return gpu_bus_utilization

# return memory utilisation values for amd gpu
def get_amd_gpu_memory_utilization():
    mem = psutil.virtual_memory()
    total_memory_mb = mem.total / (1024 ** 2)
    used_memory_mb = mem.used / (1024 ** 2)
    memory_utilization_percent = mem.percent

    return total_memory_mb, used_memory_mb, memory_utilization_percent
    
# sets attributes for hashcat
def setAttributes(self, hash):
    attributes = []
    if (tmp := self.config.get("attack-mode")) is not None:
        attributes.append("-a")
        attributes.append(getAttackMode(tmp))
        attributes.append("--runtime")
        attributes.append(getRuntime(tmp))
    attributes.append("-m")
    attributes.append(hash[0])
    attributes.append(hash[2])
    if (tmp := self.config.get("dictionaries")) is not None:
        if (tmp[len(tmp)-1] == "*"):
            for file in os.listdir(tmp[:-2]):
                attributes.append(os.path.join(tmp[:-2], file))
        else:
            attributes.append(tmp)
    if (tmp := self.config.get("charset")) is not None:
        attributes.append(tmp)
    if (tmp := self.config.get("custom-charsets")) is not None:
        if (cs := tmp.get("charset1")) is not None:
            attributes.append("-1")
            attributes.append(cs)
        if (cs := tmp.get("charset2")) is not None:
            attributes.append("-2")
            attributes.append(cs)
        if (cs := tmp.get("charset3")) is not None:
            attributes.append("-3")
            attributes.append(cs)
        if (cs := tmp.get("charset4")) is not None:
            attributes.append("-4")
            attributes.append(cs)
    if (tmp := self.config.get("increment")) is True:
        attributes.append("--increment")
    if (tmp := self.config.get("increment-min")) is not None:
        attributes.append("--increment-min")
        attributes.append(str(tmp))
    if (tmp := self.config.get("increment-max")) is not None:
        attributes.append("--increment-max")
        attributes.append(str(tmp))
    if (tmp := self.config.get("ruleset")) is not None:
        attributes.append("-r")
        attributes.append(tmp)
    if (tmp := self.config.get("device")) is not None:
        attributes.append("-d")
        attributes.append(str(tmp))
    
    return attributes

# returns runtime
def getRuntime(str):
    match str:
        case "dictionary":
            return "20"
        case "combinator":
            return "15"
        case "brute-force" | "mask":
            return "10"
        case "hybrid-a":
            return "10"
        case "hybrid-b":
            return "10"
        case "association":
            return "10"

# returns attack mode
def getAttackMode(str):
    match str:
        case "dictionary":
            return "0"
        case "combinator":
            return "1"
        case "brute-force" | "mask":
            return "3"
        case "hybrid-a":
            return "6"
        case "hybrid-b":
            return "7"
        case "association":
            return "9"

# fix the hash name so it can be saved on windows without an error        
def fixHashName(hash):
    hash = hash.replace(">", "-")
    hash = hash.replace("<", "-")
    hash = hash.replace(":", "-")
    hash = hash.replace('"', "-")
    hash = hash.replace("/", "-")
    hash = hash.replace("\\", "-")
    hash = hash.replace("|", "-")
    hash = hash.replace("?", "-")
    hash = hash.replace("*", "-")
    return hash