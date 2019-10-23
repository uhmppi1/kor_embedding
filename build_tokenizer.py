
import argparse
# import contextlib
# import sys
import sentencepiece as spm

from collections import Counter
from multiprocessing import Pool


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--input",
        # nargs="+",
        default='corpus.txt',
        help="input file to build spm model",
    )
    parser.add_argument(
        "--model_prefix",
        # nargs="+",
        default='spm_model',
        help="spm model prefix",
    )
    parser.add_argument("--vocab_size", type=int, default=1000)
    parser.add_argument("--input_sentence_size", type=int, default=1000000)
    args = parser.parse_args()

    #--mining_sentence_size = 1000000
    templates = '--input={} --model_prefix={} --vocab_size={} --model_type=bpe --max_sentence_length=16384 --input_sentence_size={} --character_coverage=0.9995 --pad_id=0 --unk_id=1 --bos_id=2 --eos_id=3 --pad_piece=[PAD] --unk_piece=[UNK] --bos_piece=[CLS] --eos_piece=[SEP] --control_symbols=[MASK]'

    print('### args.input: ', args.input)

    cmd = templates.format(args.input, args.model_prefix, args.vocab_size, args.input_sentence_size)

    spm.SentencePieceTrainer.Train(cmd)


if __name__ == "__main__":
    main()
