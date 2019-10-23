import argparse
import contextlib
import sys

from collections import Counter
from multiprocessing import Pool

from transformers import BertTokenizer
import sentencepiece as spm

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--inputs",
        nargs="+",
        default=['-'],
        help="input files to filter/encode",
    )
    parser.add_argument(
        "--outputs",
        nargs="+",
        default=['-'],
        help="path to save encoded outputs",
    )
    parser.add_argument(
        "--keep-empty",
        action="store_true",
        help="keep empty lines",
    )
    parser.add_argument("--workers", type=int, default=20)
    args = parser.parse_args()

    assert len(args.inputs) == len(args.outputs), \
        "number of input and output paths should match"

    with contextlib.ExitStack() as stack:
        inputs = [
            stack.enter_context(open(input, "r", encoding="utf-8"))
            if input != "-" else sys.stdin
            for input in args.inputs
        ]
        outputs = [
            stack.enter_context(open(output, "w", encoding="utf-8"))
            if output != "-" else sys.stdout
            for output in args.outputs
        ]

        encoder = MultiprocessingEncoder(args)
        pool = Pool(args.workers, initializer=encoder.initializer)
        encoded_lines = pool.imap(encoder.encode_lines, zip(*inputs), 100)

        stats = Counter()
        for i, (filt, enc_lines) in enumerate(encoded_lines, start=1):
            if filt == "PASS":
                for enc_line, output_h in zip(enc_lines, outputs):
                    print(enc_line, file=output_h)
            else:
                stats["num_filtered_" + filt] += 1
            if i % 10000 == 0:
                print("processed {} lines".format(i), file=sys.stderr)

        for k, v in stats.most_common():
            print("[{}] filtered {} lines".format(k, v), file=sys.stderr)


class MultiprocessingEncoder(object):

    def __init__(self, args):
        self.args = args
        # self.sp = None

    def initializer(self):
        # global bpe
        # bpe = BertTokenizer.from_pretrained('bert-base-uncased')
        # bpe = BertTokenizer.from_pretrained('bert-base-uncased')
        global sp
        # self.sp = spm.SentencePieceProcessor()
        sp = spm.SentencePieceProcessor()
        sp.Load('{}.model'.format('mass_kor_32k'))

    def encode(self, line):
        # global bpe
        global sp
        # subword = bpe._tokenize(line)
        # return subword
        return sp.EncodeAsPieces(line)

    def decode(self, tokens):
        # global bpe
        # return bpe.decode(tokens)
        global sp
        return sp.DecodePieces(tokens)

    def encode_lines(self, lines):
        """
        Encode a set of lines. All lines will be encoded together.
        """
        enc_lines = []
        for line in lines:
            line = line.strip()
            if len(line) == 0 and not self.args.keep_empty:
                return ["EMPTY", None]
            tokens = self.encode(line)
            enc_lines.append(" ".join(tokens))
        return ["PASS", enc_lines]

    def decode_lines(self, lines):
        dec_lines = []
        for line in lines:
            tokens = map(int, line.strip().split())
            dec_lines.append(self.decode(tokens))
        return ["PASS", dec_lines]


if __name__ == "__main__":
    main()
    # parser = argparse.ArgumentParser()
    # parser.add_argument(
    #     "--inputs",
    #     nargs="+",
    #     default=['-'],
    #     help="input files to filter/encode",
    # )
    # parser.add_argument(
    #     "--outputs",
    #     nargs="+",
    #     default=['-'],
    #     help="path to save encoded outputs",
    # )
    # parser.add_argument(
    #     "--keep-empty",
    #     action="store_true",
    #     help="keep empty lines",
    # )
    # parser.add_argument("--workers", type=int, default=20)
    # args = parser.parse_args()
    # encoder = MultiprocessingEncoder(args)
    # encoder.initializer()
    # sss = encoder.encode('결정적인 승부처다. 존재가 빤쓰 벗고 알몸을 들키는 결정적인 지점이 있다. 거기서 움직이는 방향이 바뀐다. ')
    # print(sss)
    # ddd = encoder.decode(sss)
    # print(ddd)
    # # for t in sss:
    # #     print(encoder.sp.IdToPiece(t))
    #
    # lines = ['원자들이 전자를 주고 받으며 공놀이를 하고 있다.',
    #          '내가 벽을 밀었기 때문에 벽이 나를 미는 것이 아니라 나와 상관없이 벽은 자체적으로 밀고 있다.',
    #          '무에서 유가 생겨날 수 없다.',
    #          '에너지 보존에 따라 이미 있는 것을 들킨다.',
    #          '자연의 모든 것은 움직인다. 움직이면 충돌한다.']
    #
    # aaa = encoder.encode_lines(lines)
    # print(aaa)
    #
