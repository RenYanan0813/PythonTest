#c:/python36/

#-*- coding: utf-8 -*-

import jieba.analyse
import matplotlib.pyplot as plt
import numpy
from wordcloud import WordCloud
from scipy.misc import imread
from pyparsing import Word, alphas
import requests
import codecs

def generate_image():
    data = []
    data1 = []
    jieba.analyse.set_stop_words("stopwords.txt")
    with codecs.open("ci.txt", 'r', encoding="utf-8") as f:
        for text in f.readlines():
            data.extend(jieba.analyse.extract_tags(text, topK=40))
            data = " ".join(data)
            mask_img = imread('../image/c.jpg', flatten=True)
            wordcloud = WordCloud(
                font_path='msyh.ttc',
                background_color='white',
                mask=mask_img ).generate(data)
            plt.imshow(wordcloud.recolor(color_func=grey_color_func, random_state=3),
                       interpolation="bilinear")
            plt.imshow(wordcloud,interpolation="bilinear")
            plt.axis('off')
            plt.savefig('../image/heart3.jpg', dpi=1600)

def grey_color_func(word, font_size, position, orientation, random_state=None,
                    **kwargs):
    s = "hsl(255, 0%%, %d%%)" % 0
    print(s)
    return s

if __name__ == '__main__':
    generate_image()

