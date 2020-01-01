import os
import warnings
from wordcloud import WordCloud, STOPWORDS

import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

warnings.filterwarnings('ignore')


class PlotUser:

    def __init__(self, user_object = None, save_path = "../plots/"):
        """

        :param user_object:
        """
        self.user_object = user_object
        self.save_path = save_path
        os.makedirs(self.save_path, exist_ok = True)

    def plot_top_k_ngrams(self, n_grams = 1, k = 10, normalize = False):
        """

        :param k:
        :return:
        """
        top_k_words = self.user_object.get_top_k_words(n_grams = n_grams, k = k, normalize = normalize)
        if normalize:
            top_k_words['Count %'] = np.round(top_k_words['Count'] * 100)
        # plt.xkcd(scale = 5, length = 400)
        plt.figure(figsize = (12, 7))
        y = 'Count'
        if normalize:
            y = 'Count %'
        g = sns.barplot(x = 'Word', y = y, data = top_k_words, color = self.user_object.user_color)
        g.set_xticklabels(g.get_xticklabels(), rotation = 90)

    def plot_word_cloud(self, n_grams = 1):
        """

        :return:
        """
        wordcloud_words = " ".join(self.user_object.get_words_for_wordcloud(n_grams = n_grams))
        if self.user_object.user_color == "#3498db":
            colormap = 'Blues'
        elif self.user_object.user_color == "#2ecc71":
            colormap = 'Greens'
        else:
            colormap = 'Reds'

        wordcloud = WordCloud(width = 500, height = 800,
                              colormap = colormap,
                              background_color = 'white', collocations = False,
                              min_font_size = 10).generate(wordcloud_words)
        plt.figure(figsize = (8, 8), facecolor = None)
        plt.imshow(wordcloud)
        plt.axis("off")
        plt.tight_layout(pad = 0)

    def plot_top_k_emojis(self, k = 10, normalize = False):
        """

        :param k:
        :return:
        """
        top_k_emojis = self.user_object.get_top_k_emojis(k = k, normalize = normalize)
        if normalize:
            top_k_emojis['Count %'] = np.round(top_k_emojis['Count'] * 100)
            top_k_emojis.drop(['Count'], axis = 1, inplace = True)
        # plt.figure(figsize = (12, 7))
        # mpl.rc('font', family = 'DejaVu Sans')
        # g = sns.barplot(x = 'Emoji', y = 'Count', data = top_k_emojis)
        return top_k_emojis