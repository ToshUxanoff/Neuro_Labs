import numpy as np

def calc_euclid_distance(x1, x2):
    result = 0
    for i in range(len(x1)):
        result += (x1[i] - x2[i]) ** 2
    result = result ** 0.5

    return result

def calc_cheb_distance(x1, x2):
    result = 0
    tmp = []
    for i in range(len(x1)):
        tmp.append(abs(x1[i] - x2[i]))
    result = max(tmp)
    return result

def calc_center_weight(clusters, old_clusters):
    res = {ind:None for ind in range(len(clusters))}
    for ind in range(len(clusters)):
        summ_x = 0
        summ_y = 0
        count = len(clusters[ind])
        if not count:
            res[ind] = old_clusters[ind]
            continue
        for coordinate in clusters[ind]:
            x, y = coordinate
            summ_x += x
            summ_y += y
    
        new_center = (np.around(summ_x / count, 2), np.around(summ_y / count, 2))
        res[ind] = new_center

    return res

def sort_points(points, clusters, flag):
    length =len(clusters)
    res = {i:[] for i in range(length)}
    for point in points:
        if not flag:
            distances = [calc_euclid_distance(point, clusters[ind]) for ind in range(length)]
        else:
            distances = [calc_cheb_distance(point, clusters[ind]) for ind in range(length)]
        ind = np.argmin(distances)
        res[ind].append(point)

    return res

def equal(old_clusters, new_clusters):
    if new_clusters is None:
        return False
    for ind in range(len(old_clusters)):
        x1, y1 = old_clusters[ind]
        x2, y2 = new_clusters[ind]
        if x1 != x2 or y1 != y2:
            return False
    return True


def process(points, clusters, flag):
    clusters = {ind:clusters[ind] for ind in range(len(clusters))}
    new_clusters = None
    point_to_clusters = sort_points(points, clusters, flag)
    new_clusters = calc_center_weight(point_to_clusters, clusters)
    return new_clusters, point_to_clusters