import numpy as np
from scipy import stats

def ztest_proportions(conversions_control, users_control, conversions_test, users_test):
    """Двухвыборочный z-тест для пропорций."""
    p1 = conversions_control / users_control
    p2 = conversions_test / users_test
    p_pool = (conversions_control + conversions_test) / (users_control + users_test)
    se = np.sqrt(p_pool * (1 - p_pool) * (1/users_control + 1/users_test))
    z = (p2 - p1) / se
    pvalue = 2 * (1 - stats.norm.cdf(abs(z)))
    return z, pvalue