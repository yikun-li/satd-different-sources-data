import argparse
import re
import string

import fasttext
import nltk
import torch
import torch.nn as nn
import torch.nn.functional as func
from torch import autograd

DEF_COMMENT = 'code_comment'
DEF_COMMIT = 'commit_message'
DEF_PULL = 'pull_request'
DEF_ISSUE = 'issue'
DEF_MAPPING = {DEF_ISSUE: 0, DEF_COMMIT: 1, DEF_COMMENT: 2, DEF_PULL: 3}
DEF_LABELS = ['non-SATD', 'code|design-debt', 'requirement-debt', 'documentation-debt', 'test-debt']


class TextCNNMultitask(nn.Module):
    """
    Text CNN multitask network based on Kim CNN structure

    """

    def __init__(self, params):
        """
        Init function

        @param params:
        """
        super(TextCNNMultitask, self).__init__()
        self.params = params

        # hyper-parameters
        self.list_conv = nn.ModuleList([nn.Conv2d(1, self.params.kernel_num, (size, self.params.embed_dim))
                                        for size in self.params.kernel_sizes])
        self.dropout = nn.Dropout(params.dropout)
        self.fcs = nn.ModuleList([nn.Linear(len(self.params.kernel_sizes) * self.params.kernel_num, class_num)
                                  for class_num in [len(DEF_LABELS) for _ in range(len(DEF_MAPPING.keys()))]])

    def forward(self, x):
        """
        Forward function

        @param x:   x shape is (batch_size, words)
        @return:
        """
        # x_embed shape is (batch_size, 1, number_of_words, embed_dim)
        # to be noted, the number_of_words varies between batches
        # this should be taken in consideration to avoid unforeseen errors
        x_embed = x.unsqueeze(1)
        # x_conv shape is (batch_size, kernel_num, feature_num)
        x_list_conv = [func.relu(conv(x_embed)).squeeze(3) for conv in self.list_conv]
        # x_max_pool shape is (batch_size, kernel_num)
        x_list_max_pool = [func.max_pool1d(x_conv, x_conv.size(2)).squeeze(2) for x_conv in x_list_conv]
        # x_concatenate and x_dropout shape is (batch_size, kernel_num * number_of_different_size_kernel)
        x_concatenate = torch.cat(x_list_max_pool, 1)
        x_dropout = self.dropout(x_concatenate)
        # x_list_logit shape is [output_num: (batch_size, class_num)]
        x_list_logit = [fc(x_dropout) for fc in self.fcs]

        return x_list_logit


class SATDDetector:
    """
    Self-admitted technical debt detector
    """

    def __init__(self, params):
        """
        Initialization

        """
        # init
        self.params = params
        self.model = None

        # load torch model
        self.load_model()
        # load word embedding
        self._pure_word_embedding = {}
        self._pure_cache_word_embedding = {}
        self._pure_word_embedding = fasttext.load_model(self.params.embed_vectors)

        self._tokenizer_words = nltk.TweetTokenizer()
        self._punctuation = string.punctuation.replace('!', '').replace('?', '')

        # set padding
        self._padding = '<pad>'

    def load_model(self):
        """
        Load model

        @return:
        """
        print('\nLoading torch model from {}...'.format(self.params.snapshot))
        model = TextCNNMultitask(params=self.params)

        if self.params.cuda:
            pretrained_dict = torch.load(self.params.snapshot)
        else:
            pretrained_dict = torch.load(self.params.snapshot, map_location=torch.device('cpu'))

        # init ignored params
        set_ignored_param = {'embed.weight'}

        # filter out embed layer
        pretrained_dict = {k: v for k, v in pretrained_dict.items() if k not in set_ignored_param}

        # overwrite entries in the existing state dict
        model_dict = model.state_dict()
        model_dict.update(pretrained_dict)

        # load the new state dict
        model.load_state_dict(model_dict)

        # if possible, enable cuda
        if self.params.cuda:
            torch.cuda.set_device(self.params.device)
            self.model = model.cuda()
        else:
            self.model = model

    def comment_pre_processing(self, comment):
        """
        Pre-process comment

        :param comment:
        :return:
        """
        comment = re.sub('(//)|(/\\*)|(\\*/)', '', comment).lower()
        tokens_sentences = [self._tokenizer_words.tokenize(t) for t in nltk.sent_tokenize(comment)]

        processed_tokens_sentences = []
        for sentence in tokens_sentences:
            processed_tokens = []
            for token in sentence:
                if token == 'non-nls' or token == self._padding:
                    processed_tokens.append(token)
                    continue
                elif token == ',':
                    processed_tokens.append('.')
                elif ' ' in token or '.' in token or '#' in token or '_' in token or '/' in token:
                    continue
                elif '>' in token or '<' in token or '@' in token:
                    continue
                elif any(char.isdigit() for char in token):
                    continue
                else:
                    processed_tokens.append(token)

            if len(processed_tokens) > 0:
                if processed_tokens[-1] != '.':
                    processed_tokens.append('.')
            processed_tokens_sentences.append(processed_tokens)

        tokens_sentences = processed_tokens_sentences
        tokens = [word for t in tokens_sentences for word in t]
        stripped = [word for word in tokens if
                    word and (word not in self._punctuation and ':' not in word and '=' not in word
                              and ')' not in word and '(' not in word)]

        return stripped

    def classify_prob_comment(self, comment, tp=None):
        """
        Classify a single comment

        :param comment:
        :param tp:
        """
        self.model.eval()
        input_x = self.comment_pre_processing(comment)
        input_x = input_x + ['<pad>'] * (5 - len(input_x))
        embed_text = []

        for word in input_x:
            if word not in self._pure_cache_word_embedding:
                word_embed = self._pure_word_embedding[word]
                self._pure_cache_word_embedding[word] = word_embed
                embed_text.append(word_embed)
            else:
                embed_text.append(self._pure_cache_word_embedding[word])

        x = autograd.Variable(torch.tensor(embed_text))
        x = x.unsqueeze(0)
        if self.params.cuda:
            x = x.cuda()
        output = self.model(x)
        _, predicted = torch.max(output[DEF_MAPPING[tp]], 1)

        print('Source type: {}\nText: {}'.format(tp, comment))
        print('Predicted result: {}\n'.format(DEF_LABELS[predicted.item()]))


def simple_test(dt):
    """
    Simple test

    :param dt:
    :return:
    """
    dt.classify_prob_comment('TODO: support multiple signers',
                             tp=DEF_COMMENT)
    dt.classify_prob_comment('TODO: please add some javadoc',
                             tp=DEF_COMMENT)
    dt.classify_prob_comment('TODO: lack of tests',
                             tp=DEF_COMMENT)
    dt.classify_prob_comment('I would like to remove this as its no longer needed.',
                             tp=DEF_ISSUE)
    dt.classify_prob_comment('to make their code more readable. I would like to see something like this in the API.',
                             tp=DEF_ISSUE)
    dt.classify_prob_comment('To experiment with transfer learning, we first combine all the issue sections',
                             tp=DEF_ISSUE)
    dt.classify_prob_comment('We need to update this documentation',
                             tp=DEF_ISSUE)
    dt.classify_prob_comment('There are unimplemented requirements',
                             tp=DEF_ISSUE)
    dt.classify_prob_comment('This is a good patch',
                             tp=DEF_ISSUE)
    dt.classify_prob_comment('Get rid of some superfluous informational messages',
                             tp=DEF_COMMIT)
    dt.classify_prob_comment('fix bugs in SystemML - removed XXX',
                             tp=DEF_COMMIT)
    dt.classify_prob_comment('fix typo in error message',
                             tp=DEF_COMMIT)
    dt.classify_prob_comment('nit: use local variable if possible',
                             tp=DEF_PULL)
    dt.classify_prob_comment('Use the Python Postinstall implementation by default',
                             tp=DEF_PULL)


def get_params():
    parser = argparse.ArgumentParser()
    parser.add_argument('--snapshot', type=str, default=None,
                        help='filename of model checkpoint [default: None]')
    parser.add_argument('--embed-vectors', type=str, default=None,
                        help='specify the path of embedding vectors [default: None]')
    parser.add_argument('--embed-dim', type=int, default=300,
                        help='number of embedding dimension [default: 300]')
    parser.add_argument('--kernel-num', type=int, default=200,
                        help='number of each kind of kernel [default: 200]')
    parser.add_argument('--kernel-sizes', nargs='+', type=int, default=[1, 2, 3, 4, 5],
                        help='comma-separated kernel size to use for convolution [default: 1, 2, 3, 4, 5]')
    parser.add_argument('--dropout', type=float, default=0.5,
                        help='the probability for dropout [default: 0.5]')
    parser.add_argument('--device', type=int, default=-1,
                        help='device to use for iterate data, -1 mean cpu [default: -1]')
    parser.add_argument('--no-cuda', action='store_true', default=False,
                        help='disable the gpu')
    args = parser.parse_args()

    # update parameters
    args.cuda = (not args.no_cuda) and torch.cuda.is_available()
    del args.no_cuda

    return args


def main():
    """
    Main func

    :return:
    """
    d = SATDDetector(get_params())
    simple_test(d)


if __name__ == '__main__':
    main()
