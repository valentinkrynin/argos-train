raise Exception('Not a runnable script')
# This script should be appended to data downloader at /data/download_data.py


# Sentence boundary detection
source_lang_data = data[0]

def strip_tail_newline(x):
    if len(x) > 0 and x[-1] == '\n':
        return x[:-1]
    return x

sbd_source = []
sbd_target = []
for i in range(len(source_lang_data)):
    # Take each sentence and add a fragment of two random sentences
    sentence = source_lang_data[i]
    rand_sentence = source_lang_data[randrange(len(source_lang_data))]
    rand_sentence2 = source_lang_data[randrange(len(source_lang_data))]
    sentence = strip_tail_newline(sentence)
    rand_sentence = strip_tail_newline(rand_sentence)
    rand_sentence2 = strip_tail_newline(rand_sentence2)
    rand_sentences = rand_sentence + rand_sentence2
    sentence_fragment = rand_sentences[:randrange(len(rand_sentences)) + 1]

    sbd_source.append('<detect-sentence-boundary>' + sentence + sentence_fragment)
    sbd_target.append(sentence + '<sentence-boundary>')

    # Include a fraction of sentences that don't contain a sentence boundary.
    # When this happens the model should return the source without the
    # <sentence-boundary> token.
    SENTENCE_BOUNDARY_MISS_RATIO = 0.1
    if random() < SENTENCE_BOUNDARY_MISS_RATIO:
        sb_miss = sentence[:randrange(len(sentence))]
        sbd_source.append('<detect-sentence-boundary>' + sb_miss)
        sbd_target.append(sb_miss)

    if i % 1000 == 0:
        print(f'Generating sbd data {i}/{len(source_lang_data)}')

# Write to file
print('Writing to file')
for filename, data in [
        ('sbd_source', sbd_source),
        ('sbd_target', sbd_target)]:
    filename = Path(filename)
    assert(not filename.exists())
    data_file = open(filename, 'w')
    data_file.write('\n'.join(data))
    data_file.close()
