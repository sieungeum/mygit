# 키워드가 포함된 클러스터 추출
import relation_dir.clusting_func_dir.get_intersection_keyword_func as gikf

def get_intersection_data(cluster_details, relation_idx, keywords):
    intersection_idx = []

    for cluster_num, cluster_detail in cluster_details.items():
        if gikf.get_intersection_keyword(keywords, cluster_detail['top_features']):
            print(f"#######cluster num : {cluster_num}")
            print()
            print("상위 20개 단어들 :\n", cluster_detail['top_features'])
            print()
            print('-' * 20)

            intersection_idx.append(relation_idx[cluster_num])
    return intersection_idx