import json

corpus_fname = 'raw/korquad/KorQuAD_v1.0_train.json'
output_fname = 'processed/processed_korquad_train.txt'

with open(corpus_fname) as f_corpus:
    with open(output_fname, 'w', encoding='utf-8') as f_output:
        dataset_json = json.load(f_corpus)
        dataset = dataset_json['data']

        for article in dataset:
            # w_lines = []
            for paragraph in article['paragraphs']:
                print('----')
                print(paragraph)
                print(paragraph['context'])
                f_output.write(paragraph['context'])
                f_output.write('\n')
                for qa in paragraph['qas']:
                    q_text = qa['question']
                    for a in qa['answers']:
                        a_text = a['text']
                        w_line = q_text + ' ' + a_text
                        print(w_line)
                        f_output.write(w_line)
                        f_output.write('\n')

                # print(paragraph)
                # for qa in paragraph['context']:
