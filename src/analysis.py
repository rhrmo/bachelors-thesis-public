import numpy as np
import os

speedIndex = 1
tempIndex = 11
utilIndex = 13
memoryIndex = 1
memory_utilIndex = 2
bus_utilIndex = 3

# count the minimum, maximum, mean and median values from the collected data
def countAverageMedianMaxMin(data, data_mem, outputFile, outputFolder, gpuName):
     if data_mem != None:
          try:
               transposedData = np.transpose(data)
               transposedData = transposedData.astype(np.float_)
               transposedDataMem = np.transpose(data_mem)
               if transposedDataMem[bus_utilIndex][0] == "":
                    transposedDataMem = transposedDataMem[:-1]
               transposedDataMem = transposedDataMem.astype(np.float_)
               median = []
               mean = []
               max = []
               min = []
               median.append(np.round(np.median(transposedData[speedIndex]), 2))
               median.append(np.round(np.median(transposedData[utilIndex]), 2))
               median.append(np.round(np.median(transposedData[tempIndex]), 2))
               median.append(np.round(np.median(transposedDataMem[memoryIndex]), 2))
               median.append(np.round(np.median(transposedDataMem[memory_utilIndex]), 2))
               if bus_utilIndex < transposedDataMem.shape[0]:
                    median.append(np.round(np.median(transposedDataMem[bus_utilIndex]), 2))
               else:
                    median.append(0)
               mean.append(np.round(np.mean(transposedData[speedIndex]), 2))
               mean.append(np.round(np.mean(transposedData[utilIndex]), 2))
               mean.append(np.round(np.mean(transposedData[tempIndex]), 2))
               mean.append(np.round(np.mean(transposedDataMem[memoryIndex]), 2))
               mean.append(np.round(np.mean(transposedDataMem[memory_utilIndex]), 2))
               if bus_utilIndex < transposedDataMem.shape[0]:
                    mean.append(np.round(np.mean(transposedDataMem[bus_utilIndex]), 2))
               else:
                    mean.append(0)
               max.append(np.round(np.max(transposedData[speedIndex]), 2))
               max.append(np.round(np.max(transposedData[utilIndex]), 2))
               max.append(np.round(np.max(transposedData[tempIndex]), 2))
               max.append(np.round(np.max(transposedDataMem[memoryIndex]), 2))
               max.append(np.round(np.max(transposedDataMem[memory_utilIndex]), 2))
               if bus_utilIndex < transposedDataMem.shape[0]:
                    max.append(np.round(np.max(transposedDataMem[bus_utilIndex]), 2))
               else:
                    max.append(0)
               min.append(np.round(np.min(transposedData[speedIndex]), 2))
               min.append(np.round(np.min(transposedData[utilIndex]), 2))
               min.append(np.round(np.min(transposedData[tempIndex]), 2))
               min.append(np.round(np.min(transposedDataMem[memoryIndex]), 2))
               min.append(np.round(np.min(transposedDataMem[memory_utilIndex]), 2))
               if bus_utilIndex < transposedDataMem.shape[0]:
                    min.append(np.round(np.min(transposedDataMem[bus_utilIndex]), 2))
               else:
                    min.append(0)
               outputFile = outputFile.split("-", 1)
               file=open(os.path.join(outputFolder, "results", outputFile[1]), "a")
               if(os.stat(os.path.join(outputFolder, "results", outputFile[1])).st_size == 0):
                    file.write("GPU,CONFIG,SPEED_MIN,SPEED_MAX,SPEED_MEAN,SPEED_MEDIAN,UTIL_MIN,UTIL_MAX,UTIL_MEAN,UTIL_MEDIAN,TEMP_MIN,TEMP_MAX,TEMP_MEAN,TEMP_MEDIAN,MEM_USED_MIN,MEM_USED_MAX,MEM_USED_MEAN,MEM_USED_MEDIAN,MEM_UTIL_MIN,MEM_UTIL_MAX,MEM_UTIL_MEAN,MEM_UTIL_MEDIAN,BUS_UTIL_MIN,BUS_UTIL_MAX,BUS_UTIL_MEAN,BUS_UTIL_MEDIAN\n")
               file.write(
                    gpuName + "," +
                    outputFile[0] + "," +
                    str(min[0]) + "," +
                    str(max[0]) + "," +
                    str(mean[0]) + "," +
                    str(median[0]) + "," +
                    str(min[1]) + "," +
                    str(max[1]) + "," +
                    str(mean[1]) + "," +
                    str(median[1]) + "," +
                    str(min[2]) + "," +
                    str(max[2]) + "," +
                    str(mean[2]) + "," +
                    str(median[2]) + "," +
                    str(min[3]) + "," +
                    str(max[3]) + "," +
                    str(mean[3]) + "," +
                    str(median[3]) + "," +
                    str(min[4]) + "," +
                    str(max[4]) + "," +
                    str(mean[4]) + "," +
                    str(median[4]) + "," +
                    str(min[5]) + "," +
                    str(max[5]) + "," +
                    str(mean[5]) + "," +
                    str(median[5]) + "," + "\n"
               )

               file=open(os.path.join(outputFolder, "results-together", outputFile[0] + ".csv"), "a")
               if(os.stat(os.path.join(outputFolder, "results-together", outputFile[0] + ".csv")).st_size == 0):
                    file.write("GPU,HASH,CONFIG,SPEED_MIN,SPEED_MAX,SPEED_MEAN,SPEED_MEDIAN,UTIL_MIN,UTIL_MAX,UTIL_MEAN,UTIL_MEDIAN,TEMP_MIN,TEMP_MAX,TEMP_MEAN,TEMP_MEDIAN,MEM_USED_MIN,MEM_USED_MAX,MEM_USED_MEAN,MEM_USED_MEDIAN,MEM_UTIL_MIN,MEM_UTIL_MAX,MEM_UTIL_MEAN,MEM_UTIL_MEDIAN,BUS_UTIL_MIN,BUS_UTIL_MAX,BUS_UTIL_MEAN,BUS_UTIL_MEDIAN\n")
               file.write(
                    gpuName + "," +
                    os.path.splitext(outputFile[1])[0].replace(",", " ") + "," +
                    outputFile[0] + "," +
                    str(min[0]) + "," +
                    str(max[0]) + "," +
                    str(mean[0]) + "," +
                    str(median[0]) + "," +
                    str(min[1]) + "," +
                    str(max[1]) + "," +
                    str(mean[1]) + "," +
                    str(median[1]) + "," +
                    str(min[2]) + "," +
                    str(max[2]) + "," +
                    str(mean[2]) + "," +
                    str(median[2]) + "," + 
                    str(min[3]) + "," +
                    str(max[3]) + "," +
                    str(mean[3]) + "," +
                    str(median[3]) + "," +
                    str(min[4]) + "," +
                    str(max[4]) + "," +
                    str(mean[4]) + "," +
                    str(median[4]) + "," +
                    str(min[5]) + "," +
                    str(max[5]) + "," +
                    str(mean[5]) + "," +
                    str(median[5]) + "," + "\n"
               )
          except Exception as error:
               if str(error).find("setting an array element") != -1:
                    print("countAverageMedianMax() error:")
                    print("error file:" + outputFile)
                    print(error)
               pass
     else:
          try:
               transposedData = np.transpose(data)
               transposedData = transposedData.astype(np.float_)
               median = []
               mean = []
               max = []
               min = []
               median.append(np.round(np.median(transposedData[speedIndex]), 2))
               median.append(np.round(np.median(transposedData[utilIndex]), 2))
               median.append(np.round(np.median(transposedData[tempIndex]), 2))
               mean.append(np.round(np.mean(transposedData[speedIndex]), 2))
               mean.append(np.round(np.mean(transposedData[utilIndex]), 2))
               mean.append(np.round(np.mean(transposedData[tempIndex]), 2))
               max.append(np.round(np.max(transposedData[speedIndex]), 2))
               max.append(np.round(np.max(transposedData[utilIndex]), 2))
               max.append(np.round(np.max(transposedData[tempIndex]), 2))
               min.append(np.round(np.min(transposedData[speedIndex]), 2))
               min.append(np.round(np.min(transposedData[utilIndex]), 2))
               min.append(np.round(np.min(transposedData[tempIndex]), 2))
               outputFile = outputFile.split("-", 1)
               file=open(os.path.join(outputFolder, "results", outputFile[1]), "a")
               if(os.stat(os.path.join(outputFolder, "results", outputFile[1])).st_size == 0):
                    file.write("GPU,CONFIG,SPEED_MIN,SPEED_MAX,SPEED_MEAN,SPEED_MEDIAN,UTIL_MIN,UTIL_MAX,UTIL_MEAN,UTIL_MEDIAN,TEMP_MIN,TEMP_MAX,TEMP_MEAN,TEMP_MEDIAN,MEM_USED_MIN,MEM_USED_MAX,MEM_USED_MEAN,MEM_USED_MEDIAN,MEM_UTIL_MIN,MEM_UTIL_MAX,MEM_UTIL_MEAN,MEM_UTIL_MEDIAN,BUS_UTIL_MIN,BUS_UTIL_MAX,BUS_UTIL_MEAN,BUS_UTIL_MEDIAN\n")
               file.write(
                    gpuName + "," +
                    outputFile[0] + "," +
                    str(min[0]) + "," +
                    str(max[0]) + "," +
                    str(mean[0]) + "," +
                    str(median[0]) + "," +
                    str(min[1]) + "," +
                    str(max[1]) + "," +
                    str(mean[1]) + "," +
                    str(median[1]) + "," +
                    str(min[2]) + "," +
                    str(max[2]) + "," +
                    str(mean[2]) + "," +
                    str(median[2]) + "," +
                    "" + "," +
                    "" + "," +
                    "" + "," +
                    "" + "," +
                    "" + "," +
                    "" + "," +
                    "" + "," +
                    "" + "," +
                    "" + "," +
                    "" + "," +
                    "" + "," +
                    "" + "," + "\n"
               )

               file=open(os.path.join(outputFolder, "results-together", outputFile[0] + ".csv"), "a")
               if(os.stat(os.path.join(outputFolder, "results-together", outputFile[0] + ".csv")).st_size == 0):
                    file.write("GPU,HASH,CONFIG,SPEED_MIN,SPEED_MAX,SPEED_MEAN,SPEED_MEDIAN,UTIL_MIN,UTIL_MAX,UTIL_MEAN,UTIL_MEDIAN,TEMP_MIN,TEMP_MAX,TEMP_MEAN,TEMP_MEDIAN,MEM_USED_MIN,MEM_USED_MAX,MEM_USED_MEAN,MEM_USED_MEDIAN,MEM_UTIL_MIN,MEM_UTIL_MAX,MEM_UTIL_MEAN,MEM_UTIL_MEDIAN,BUS_UTIL_MIN,BUS_UTIL_MAX,BUS_UTIL_MEAN,BUS_UTIL_MEDIAN\n")
               file.write(
                    gpuName + "," +
                    os.path.splitext(outputFile[1])[0].replace(",", " ") + "," +
                    outputFile[0] + "," +
                    str(min[0]) + "," +
                    str(max[0]) + "," +
                    str(mean[0]) + "," +
                    str(median[0]) + "," +
                    str(min[1]) + "," +
                    str(max[1]) + "," +
                    str(mean[1]) + "," +
                    str(median[1]) + "," +
                    str(min[2]) + "," +
                    str(max[2]) + "," +
                    str(mean[2]) + "," +
                    str(median[2]) + "," + 
                    "" + "," +
                    "" + "," +
                    "" + "," +
                    "" + "," +
                    "" + "," +
                    "" + "," +
                    "" + "," +
                    "" + "," +
                    "" + "," +
                    "" + "," +
                    "" + "," +
                    "" + "," + "\n"
               )
          except Exception as error:
               if str(error).find("setting an array element") != -1:
                    print("countAverageMedianMax() error:")
                    print("error file:" + outputFile)
                    print(error)
               pass
