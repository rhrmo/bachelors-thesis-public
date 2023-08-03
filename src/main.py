import argparse
import csv
import os
import yaml
import hashcat as hs
import analysis

# main function
def main():
    parser = argparse.ArgumentParser(description="The program for testing GPUs and then preparing collected data for analysis.") #TODO add description
    parser.add_argument("-i", "--input", help = "input folder with hashcat test settings")
    parser.add_argument("-hs", "--hashes", help = "input file with hashes")
    parser.add_argument("-hf", "--hashfiles", help = "input folder location of files with hashes")
    parser.add_argument("-hp", "--hashcatpath", help = "input hashcat path")
    parser.add_argument("-o", "--output", help = "set output folder path", required=True)
    parser.add_argument("-a", "--analysis", action=argparse.BooleanOptionalAction, help = "creates CSV file for the analysis")
    parser.add_argument("--amd", action=argparse.BooleanOptionalAction, help ="Run with this parameter if you have AMD graphics card")
    parser.set_defaults(analysis=False)
    parser.set_defaults(amd=False)

    args = parser.parse_args()
    if args.analysis == False:
        if args.input is None:
            print("Argument ERROR: --input is required argument")
            quit()
        if args.hashes is None:
            print("Argument ERROR: --hashes is required argument")
            quit()
        if args.hashfiles is None:
            print("Argument ERROR: --hashfiles is required argument")
            quit()
        if args.hashcatpath is None:
            print("Argument ERROR: --hashcatpath is required argument")
            quit()

    outputFolder = args.output

    if(args.analysis == False):
        if (os.path.isdir(outputFolder) == False):
            os.mkdir(outputFolder) 

        hashcat = hs.Hashcat(None, args.hashcatpath, None)
        gpuName = hashcat.getGpuName()

        potfile = os.path.splitext(hashcat.hsPath)[0] + ".potfile"

        benchmarkFolder = os.path.join(outputFolder, "benchmark")
        if (os.path.isdir(benchmarkFolder) == False):
            os.mkdir(benchmarkFolder)

        gpusFolder = os.path.join(outputFolder, "GPUs")
        if (os.path.isdir(gpusFolder) == False):
            os.mkdir(gpusFolder)

        gpuFolder = os.path.join(gpusFolder, gpuName)
        if (os.path.isdir(gpuFolder) == False):
            os.mkdir(gpuFolder)

        memory_dataFolder = os.path.join(gpuFolder, "memory_data")
        if (os.path.isdir(memory_dataFolder) == False):
            os.mkdir(memory_dataFolder)

        outputDataFolder = os.path.join(gpuFolder, "data")
        if (os.path.isdir(outputDataFolder) == False):
            os.mkdir(outputDataFolder)

        hashcat.outputPath = outputDataFolder
        hashcat.dummy()
        if (os.path.isfile(potfile) == True):
            os.remove(potfile)
        hashcat.benchmark(benchmarkFolder, gpuName)
        for filename in os.listdir(args.input):
            with open(os.path.join(args.input, filename), "r") as stream:
                try:
                    config = yaml.safe_load(stream)
                except yaml.YAMLError as exc:
                    raise ValueError(exc)
            hashcat.config = config
            with open(args.hashes, "r", encoding="utf-8") as csv_file:
                hashesFromFiles = False
                csv_reader = csv.reader(csv_file, delimiter="|")
                for hash in csv_reader:
                    if hash[0] == "hashes from files":
                        hashesFromFiles = True
                        continue
                    try:
                        if hashesFromFiles == False:
                            hashcat.runHashcat(hash, "", potfile, filename, memory_dataFolder, args.amd)
                        else:
                            hashcat.runHashcat(hash, args.hashfiles, potfile, filename, memory_dataFolder, args.amd)
                    except:
                        try:
                            if hashesFromFiles == False:
                                hashcat.runHashcat(hash, "", potfile, filename, memory_dataFolder, args.amd)
                            else:
                                hashcat.runHashcat(hash, args.hashfiles, potfile, filename, memory_dataFolder, args.amd)
                        except Exception as e:
                            print("ERROR: couldnt run hashcat or save the output")
                            try:
                                print(e)
                            except:
                                print("couldn't print error")
                            continue
    else:
        if (os.path.isdir(outputFolder) == False):
            print("ERROR: No output folder with data.")
            quit()
        gpusFolder = os.path.join(outputFolder, "GPUs")
        if (os.path.isdir(gpusFolder) == False):
            print("ERROR: GPUs folder is empty")
            quit()
        resultsFolder = os.path.join(outputFolder, "results")
        if (os.path.isdir(resultsFolder) == False):
            os.mkdir(resultsFolder)
        resultsFolder = os.path.join(outputFolder, "results-together")
        if (os.path.isdir(resultsFolder) == False):
            os.mkdir(resultsFolder)
        for folder in os.listdir(gpusFolder):
            gpuDataFolder = os.path.join(gpusFolder, folder, "data")
            gpuMemoryFolder = os.path.join(gpusFolder, folder, "memory_data")
            for filename in os.listdir(gpuDataFolder):
                print(folder + " " + filename)
                file = os.path.join(gpuDataFolder, filename)
                file_mem = os.path.join(gpuMemoryFolder, filename)
                with open(file, "r") as csv_file:
                    csv_reader = list(csv.reader(csv_file, delimiter=","))
                    endIndex = 1
                    for index, line in enumerate(csv_reader):
                        if line[0].startswith("err"):
                            endIndex = index
                            break
                    try:
                        with open(file_mem, "r") as csv_file_mem:
                            csv_reader_mem = list(csv.reader(csv_file_mem, delimiter=","))
                            analysis.countAverageMedianMaxMin(csv_reader[1:endIndex], csv_reader_mem[1:], filename, outputFolder, folder)
                    except:
                        analysis.countAverageMedianMaxMin(csv_reader[1:endIndex], None, filename, outputFolder, folder)


if __name__ == "__main__":
    main()