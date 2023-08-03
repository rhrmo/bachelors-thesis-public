import os
import re
import csv

#save hashcat output into a csv file
def saveOutput(out, err, filepath, args, mem_total, mem_used, mem_util, bus_util, mem_filepath):
    partition = out.partition("STATUS")
    data = partition[1] + partition[2]
    data = ",".join(data.split("\t"))
    output = "STATUS,SPEED,MILISECONDS,EXEC_RUNTIME,CURKU,PROGRESS,PROGRESS_ALL,RECHASH,RECHASH,RECSALT,RECSALT,TEMP,REJECTED,UTIL"
    for column in data.split()[3:]:
        output += "\n"
        info = re.findall("[-+]?[.]?[\d]+(?:,\d\d\d)*[\.]?\d*(?:[eE][-+]?\d+)?", column)
        output += ",".join(info)
    output += ("\nerr," +err)
    output += ("\nhashcat arguments," + " ".join(args))
    with open(filepath + ".csv", 'w', newline="\r\n") as file:
        file.write(output)
    
    transposed_lists = list(zip(mem_total, mem_used, mem_util, bus_util))
    header = ["MEMORY_MAX", "MEMORY_USED", "MEMORY_UTIL", "BUS_UTIL"]
    csv_file = mem_filepath  + ".csv"
    with open(csv_file, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(header)
        writer.writerows(transposed_lists)

#save output of benchmark
def saveBM(out, err, folder, gpuName):
    output = "ID:HASH:?:EXEC_RUNTIME:hashes/s\n"
    output += out
    output += "err:"
    output += err
    print(output, file=open(os.path.join(folder, gpuName + ".csv"), 'w', newline=''))