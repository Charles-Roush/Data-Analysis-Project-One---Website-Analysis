import numpy as np

def get_basic_stats(data):
    stats = {
            'mean': np.mean(data),
            'median': np.median(data),
            'var': np.var(data),
            'std': np.std(data),
            'min': min(data),
            'max': max(data)
    }
    return stats

def get_quartiles(data):
    return np.percentile(data, [25, 50, 75])