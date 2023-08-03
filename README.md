# Analysis Tool README
To use the tool you need to have at least Python version `3.10`.To use the analysis mode of the tool you first need to uncompress data under folder\GPUs.

## Launching the Tool
Launching the tool is done by using the Windows command line interface. We launch the tool by using python3 `src\main.py`.
### Explanation of Arguments 
```
.\python3 main.py [-h] [-i INPUT] [-hs HASHES] [-hf HASHFILES] [-hp HASHCATPATH] -o OUTPUT [-a | --analysis | --no-analysis] [--amd | --no-amd]
```

- `-h --help` - show this help message and exit
- `-i INPUT, --input INPUT` - input folder with hashcat test settings
- `-hs HASHES, --hashes HASHES` - input file with hashes
- `-hf HASHFILES, --hashfiles HASHFILES` - input folder location of files with hashes
- `-hp HASHCATPATH, --hashcatpath HASHCATPATH` - input hashcat path
- `-o OUTPUT, --output OUTPUT` - set output folder path
- `-a, --analysis, --no-analysis` - creates CSV file for the analysis
- `--amd` - run with this parameter if you have AMD graphics card

## Required Python Modules
The required Python modules are: `numpy`, `os`, `subprocess`, `pynvml`, `time`, `psutil`, `csv`, `argparse`, `yaml` and `re`.

## Required Wordlist
If you want to test your own GPU you need to download the rockyou wordlist from https://github.com/brannondorsey/naive-hashcat/releases/download/data/rockyou.txt and put it into `dictionaries-dict\`.

## Required data
If you want to use the analysis mode with the collected data you need to unzip them under the output\GPUs\ repository.