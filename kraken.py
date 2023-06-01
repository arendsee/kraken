import subprocess
import io
import pandas as pd
import tempfile
import os
import sys

kraken_report_column_names = ["classified", "sequenceId", "taxon", "length", "LCA"]
kraken_report_summary_names = ["percent_abundance", "count", "countNode", "taxon", "rank"]

#  isgzF :: Filename -> Bool
def has_extension(filename, extension, terminal=True):
    extensions = filename.split(".")[1:]
    if terminal:
        return extension == extensions[-1]
    else:
        return extension in extensions

def isGzipF(filename):
    return has_extension(filename, "gz", terminal=True)

def isFastqF(filename):
    return has_extension(filename, "fastq", terminal=False) or has_extension(filename, "fq", terminal=False)


def krakenPaired(config, r1file, r2file):
    opts = []

    if(isGzipF(r1file) and isGzipF(r2file)):
        opts.append("--gzip-compressed")

    if(isFastqF(r1file) and isFastqF(r2file)):
        opts.append("--fastq-input")

    result = subprocess.run([
        "kraken",
        *opts,
        "--threads", str(config["threads"]),
        "--paired",
        "--preload",
        "--db",
        config["db"],
        r1file,
        r2file,
    ], capture_output=True, encoding="ascii")

    if(result.returncode == 0):
        return pd.read_csv(
            io.StringIO(result.stdout), # FIXME: This step is inefficient, I should directly use the STDOUT file
            sep="\t", # type:ignore
            names=kraken_report_column_names, # type:ignore
        )
    else:
        raise Exception(result.stderr)


def krakenReport(config, krakenOutputTable):
    result = subprocess.run(
        [ "kraken-report", "--db", config["db"]],
        krakenOutputTable.to_csv(sep="\t", header=False),
        capture_output=True,
        encoding="ascii",
        )
    if(result.returncode == 0):
        return pd.read_csv(
            io.StringIO(result.stdout), # FIXME: This step is inefficient, I should directly use the STDOUT file
            sep="\t", # type:ignore
            names=kraken_summary_column_names, # type:ignore
        )
    else:
        raise Exception(result.stderr)

def readKrakenReport(filename):
    return pd.read_csv(
        filename,
        sep="\t", # type:ignore
        names=kraken_report_column_names, # type:ignore
    )

def krakenMPA(config, krakenOutputTable):
    with tempfile.NamedTemporaryFile(delete=False) as tmp:
        krakenOutputTable.to_csv(tmp.name, sep="\t", index=False, header=False)
        tmp_filename = tmp.name

    try:
        result = subprocess.run(
            ["kraken-mpa-report", "--db", config["db"], tmp_filename],
            capture_output=True,
            encoding="ascii",
        )

        if result.returncode == 0:
            mpa = dict()
            for line in result.stdout.strip().split("\n"):
                (lineage, count) = line.split("\t")
                mpa[lineage] = int(count)
            return mpa
        else:
            raise Exception(result.stderr)
    finally:
        os.remove(tmp_filename)

def writeMPA(filename, mpa):
    with open(filename, "w") as f:
        for (lineage, count) in mpa.items():
            print(f"{lineage}\t{count}", file=f)


def krakenVersion():
    result = subprocess.run(["kraken", "-v"], capture_output=True, encoding="ascii")
    if result.returncode == 0:
        return result.stdout.strip()
    else:
        return "kraken executable not found"


def krakenHelp():
    result = subprocess.run(["kraken", "-h"], capture_output=True, encoding="ascii")
    if result.returncode == 0:
        return result.stderr.strip()
    else:
        return "kraken executable not found"
