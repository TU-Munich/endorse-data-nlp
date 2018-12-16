from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

analyzer = SentimentIntensityAnalyzer()


def sentences_sentiment(sentences):
    count = len(sentences)

    result = dict()
    result["total"] = dict()
    result["total"]["compound"]=0
    result["total"]["neg"]=0
    result["total"]["neu"]=0
    result["total"]["pos"]=0
    result["sentences"] = []

    for sentence in sentences:
        vs = analyzer.polarity_scores(sentence)
        res = dict()
        res["input"] = sentence
        res["sentiment"] = vs
        # total
        result["total"]["compound"] += vs["compound"]
        result["total"]["neg"] += vs["neg"]
        result["total"]["neu"] += vs["neu"]
        result["total"]["pos"] += vs["pos"]

        result["sentences"].append(res)

    # overall
    result["total"]["neg"] = result["total"]["neg"] / count
    result["total"]["neu"] = result["total"]["neu"] / count
    result["total"]["pos"] = result["total"]["pos"] / count

    return result
