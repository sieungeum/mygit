def get_intersection_keyword(keywords, cluster_features):
    if len(set(keywords) & set(cluster_features)) == len(keywords):
        return True
    else:
        return False