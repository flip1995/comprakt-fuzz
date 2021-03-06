import gramfuzz
import os
import uuid
from argparse import ArgumentParser


def main():
    parser = ArgumentParser()
    parser.add_argument("-o", "--out", dest="out_dir",
                        default="output/",
                        help="the output directory for the fuzzed files")
    parser.add_argument("-n", dest="num", default="10", type=int,
                        help="number of files that should be produced")
    parser.add_argument("--vim_format", dest="vim_format", action="store_true",
                        help="format the output files with vim")

    args = parser.parse_args()

    if not os.path.exists(args.out_dir):
        os.makedirs(args.out_dir)

    fuzzer = gramfuzz.GramFuzzer()
    fuzzer.load_grammar(os.path.join(os.path.dirname(os.path.abspath(__file__)), "minijava_grammar.py"))
    minijava = fuzzer.gen(cat="minijava", num=args.num, auto_process=False)

    for i in range(0, args.num):
        filename = args.out_dir + "/" + uuid.uuid4().hex + ".java"
        with open(filename, "w") as file:
            file.write(minijava[i])

        if args.vim_format:
            os.system("""vim +"execute 'normal! =G' | :wq! """ + filename + """" """ + filename)
