import os
import glob
from nltk.tokenize import TreebankWordTokenizer

def build_vocab(filepaths, dst_path, lowercase=True):
    """
    Builds a vocabulary list for the dataset
    """
    vocab = set()
    for filepath in filepaths:
        with open(filepath) as f:
            for line in f:
                if lowercase:
                    line = line.lower()
                vocab |= set(line.split())
    with open(dst_path, 'w') as f:
        for w in sorted(vocab):
            f.write(w + '\n')


def dump(data, outfile):
    with open(outfile, 'w') as outf:
        outf.write('\n'.join(data) + '\n')


def write_out(infile, out_folder):
    if not os.path.exists(out_folder):
        os.mkdir(out_folder)

    qfile = open(os.path.join(out_folder, 'a.toks'), 'w')
    afile = open(os.path.join(out_folder, 'b.toks'), 'w')
    lfile = open(os.path.join(out_folder, 'sim.txt'), 'w')

    qids = []
    questions = []
    answers = []
    labels = []

    tokenizer = TreebankWordTokenizer()

    qid_count = 0
    qid_old = None
    qid_labels = []
    qid_questions = []
    qid_answers = []
    qid_qids = []
    with open(infile) as inf:
        inf.readline() # header
        for line in inf:
            fields = line.lower().strip().split('\t')
            qid = fields[0]
            question = ' '.join(tokenizer.tokenize(fields[1]))
            sentence = ' '.join(tokenizer.tokenize(fields[5])[:40])
            label = fields[6]
            if qid != qid_old:
                qid_old = qid
                qid_count += 1
                if "1" in qid_labels:
                    qids.extend(qid_qids)
                    questions.extend(qid_questions)
                    answers.extend(qid_answers)
                    labels.extend(qid_labels)
                qid_labels = []
                qid_questions = []
                qid_answers = []
                qid_qids = []
            qid_qids.append(str(qid_count))
            qid_questions.append(question)
            qid_answers.append(sentence)
            qid_labels.append(label)

    dump(questions, os.path.join(out_folder, 'a.toks'))
    dump(answers, os.path.join(out_folder, 'b.toks'))
    dump(labels, os.path.join(out_folder, 'sim.txt'))
    dump(qids, os.path.join(out_folder, 'id.txt'))



if __name__ == "__main__":

    write_out(os.path.join('WikiQACorpus', 'WikiQA-train.tsv'), 'train')
    write_out(os.path.join('WikiQACorpus', 'WikiQA-dev.tsv'), 'dev')
    write_out(os.path.join('WikiQACorpus', 'WikiQA-test.tsv'), 'test')

    build_vocab(
        glob.glob(os.path.join('.', '*/*.toks')),
        os.path.join('.', 'vocab.txt'), False)
