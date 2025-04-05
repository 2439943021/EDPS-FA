import nltk

def split_sentences(text):
    """
    将文章切割句子
    @param text:
    @return:
    """
    sentences = nltk.sent_tokenize(text)
    return sentences
