def calc_TFIDF(frequencyTokens, totalTokens, numberOfResources, totalResourceAppears):
    weight = (frequencyTokens/totalTokens) * (numberOfResources/totalResourceAppears)
    return weight