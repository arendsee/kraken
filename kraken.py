import subprocess
import io
import pandas as pd

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
        pd.to_csv(krakenOutputTable, sep="\t", header=False),
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


def krakenMPA(config, krakenOutputTable):
    result = subprocess.run(
        [ "kraken-mpa-report", "--db", config["db"]],
        pd.to_csv(krakenOutputTable, sep="\t", header=False),
        capture_output=True,
        encoding="ascii",
        )
    if(result.returncode == 0):
        mpa = dict()
        for line in result.stdout:
            (lineage, count) = line.split("\t")
            mpa[lineage] = int(count)
        return mpa
    else:
        raise Exception(result.stderr)


def writeMPA(table):
    pass


def writeReport(table):
    pass


def readKrakenReport(filename):
    return pd.read_csv(filename, sep="\t", names=kraken_report_column_names) # type:ignore


def readKrakenSummary(filename):
    return pd.read_csv(filename, sep="\t", names=kraken_summary_column_names) # type:ignore


def krakenVersion():
    result = subprocess.run(["kraken", "-v"], capture_output=True, encoding="ascii")
    if result.returncode == 0:
        return result.stdout
    else:
        raise Exception(result.stderr)


def krakenHelp():
    result = subprocess.run(["kraken", "-h"], capture_output=True, encoding="ascii")
    if result.returncode == 0:
        return result.stderr
    else:
        raise Exception(result.stderr)


#  Usage: kraken [options] <filename(s)>
#
#  Options:
#    --db NAME               Name for Kraken DB
#                            (default: none)
#    --threads NUM           Number of threads (default: 1)
#    --fasta-input           Input is FASTA format
#    --fastq-input           Input is FASTQ format
#    --fastq-output          Output in FASTQ format
#    --gzip-compressed       Input is gzip compressed
#    --bzip2-compressed      Input is bzip2 compressed
#    --quick                 Quick operation (use first hit or hits)
#    --min-hits NUM          In quick op., number of hits req'd for classification
#                            NOTE: this is ignored if --quick is not specified
#    --unclassified-out FILENAME
#                            Print unclassified sequences to filename
#    --classified-out FILENAME
#                            Print classified sequences to filename
#    --out-fmt FORMAT        Format for [un]classified sequence output. supported
#                            options are: {legacy, paired, interleaved}
#    --output FILENAME       Print output to filename (default: stdout); "-" will
#                            suppress normal output
#    --only-classified-output
#                            Print no Kraken output for unclassified sequences
#    --preload               Loads DB into memory before classification
#    --paired                The two filenames provided are paired-end reads
#    --check-names           Ensure each pair of reads have names that agree
#                            with each other; ignored if --paired is not specified
#    --help                  Print this message
#    --version               Print version information
#
#  If none of the *-input or *-compressed flags are specified, and the
#  file is a regular file, automatic format detection is attempted.
