# 교집합된 클러스터 찾는 함수
def get_cluster_details(cluster_model, cluster_data, feature_names, cluster_num, top_n_features=20):
    cluster_details = {}
    relation_idxs = []  # 교집합인 데이터들의 인덱스 저장할 리스트

    # 각 클러스터들의 상위 학습 단어 인덱스
    center_featrue_idx = cluster_model.cluster_centers_.argsort()[:, ::-1]

    for cluster_num in range(cluster_num):
        cluster_details[cluster_num] = {}
        cluster_details[cluster_num]['cluster'] = cluster_num

        top_ftr_idx = center_featrue_idx[cluster_num, :top_n_features]
        top_ftr = [feature_names[idx] for idx in top_ftr_idx]

        cluster_details[cluster_num]['top_features'] = top_ftr

        # 각 클러스터 뉴스 기사들
        content = cluster_data[cluster_data['cluster_label'] == cluster_num]['content']

        # 교집합인 데이터들의 인덱스 저장
        arr = []
        for idx in content.keys():
            arr.append(idx)
        relation_idxs.append(arr)

        # 각 클러스터 뉴스 기사들 저장
        content = content.values.tolist()
        cluster_details[cluster_num]['content'] = content

    return cluster_details, relation_idxs