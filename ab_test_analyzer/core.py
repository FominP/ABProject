import numpy as np
from scipy.stats import t, chi2, norm

def ztest_proportions(conversions_control, users_control, conversions_test, users_test):
    """
    Двухвыборочный z-тест для пропорций.
    """
    p1 = conversions_control / users_control
    p2 = conversions_test / users_test
    p_pool = (conversions_control + conversions_test) / (users_control + users_test)
    se = np.sqrt(p_pool * (1 - p_pool) * (1/users_control + 1/users_test))
    z = (p2 - p1) / se
    p_value = 2 * (1 - norm.cdf(abs(z)))
    return {
        'z_score': z,
        'p_value': p_value
    }

def ttest_means(mean_control, mean_test, std_control, std_test, n_control, n_test):
    """
    Двухвыборочный t-тест для средних (неравные дисперсии, тест Уэлча).
    Принимает средние, стандартные отклонения и размеры выборок.
    """
    se = np.sqrt(std_control**2 / n_control + std_test**2 / n_test)
    t_stat = (mean_test - mean_control) / se
    # Степени свободы по формуле Уэлча-Сатертуэйта
    df = ( (std_control**2 / n_control + std_test**2 / n_test)**2 ) / \
         ( (std_control**4 / (n_control**2 * (n_control - 1))) + \
           (std_test**4 / (n_test**2 * (n_test - 1))) )
    p_value = 2 * (1 - t.cdf(abs(t_stat), df))
    return {
        't_statistic': t_stat,
        'df': df,
        'p_value': p_value
    }

def chi_square_test(observed, expected=None):
    """
    Тест хи-квадрат для таблицы сопряжённости 2x2.
    observed : list/tuple из четырёх чисел [a, b, c, d]
               a - конверсии в контроле, b - конверсии в тесте,
               c - не-конверсии в контроле, d - не-конверсии в тесте.
    Если expected не задан, то вычисляется по маргинальным частотам.
    """
    a, b, c, d = observed
    n = a + b + c + d
    if expected is None:
        # Ожидаемые частоты при нулевой гипотезе
        row1 = a + b
        row2 = c + d
        col1 = a + c
        col2 = b + d
        e_a = row1 * col1 / n
        e_b = row1 * col2 / n
        e_c = row2 * col1 / n
        e_d = row2 * col2 / n
        expected = [e_a, e_b, e_c, e_d]
    else:
        e_a, e_b, e_c, e_d = expected

    chi2_stat = 0.0
    for obs, exp in zip(observed, expected):
        if exp != 0:
            chi2_stat += (obs - exp)**2 / exp
    df = 1  # для 2x2 таблицы
    p_value = 1 - chi2.cdf(chi2_stat, df)
    return {
        'chi2_statistic': chi2_stat,
        'df': df,
        'p_value': p_value
    }

def check_srm(users_control, users_test, expected_ratio=0.5):
    """
    Проверка Sample Ratio Mismatch (SRM) с помощью хи-квадрат.
    users_control, users_test – размеры групп.
    expected_ratio – ожидаемая доля пользователей в группе test (от общего числа).
    Возвращает p-value для гипотезы о соответствии наблюдаемого соотношения ожидаемому.
    """
    total = users_control + users_test
    observed = [users_control, users_test]
    expected = [total * (1 - expected_ratio), total * expected_ratio]
    chi2_stat = 0.0
    for obs, exp in zip(observed, expected):
        if exp != 0:
            chi2_stat += (obs - exp)**2 / exp
    df = 1
    p_value = 1 - chi2.cdf(chi2_stat, df)
    return {
        'chi2_statistic': chi2_stat,
        'p_value': p_value,
        'observed_ratio': users_test / total,
        'expected_ratio': expected_ratio
    }

def calculate_mde(baseline_conversion, alpha=0.05, power=0.8, n_control=None, n_test=None, equal_size=True):
    """
    Минимально детектируемый эффект (MDE) для двухвыборочного z-теста пропорций.
    Если выборки разного размера, укажите n_control и n_test.
    equal_size=True означает, что n_control = n_test (тогда достаточно n_control).
    Возвращает абсолютный MDE (разницу в конверсиях) и относительный MDE (%).
    """
    if equal_size:
        if n_control is None:
            raise ValueError("При equal_size=True нужно указать n_control")
        n_test = n_control
    elif n_control is None or n_test is None:
        raise ValueError("При equal_size=False укажите n_control и n_test")

    z_alpha = norm.ppf(1 - alpha/2)
    z_beta = norm.ppf(power)
    p1 = baseline_conversion
    n_eff = 2 * n_control * n_test / (n_control + n_test)   # гармоническое среднее
    mde_abs = (z_alpha + z_beta) * np.sqrt(2 * p1 * (1 - p1) / n_eff)
    mde_rel = mde_abs / p1 * 100
    return {
        'mde_absolute': mde_abs,
        'mde_relative_percent': mde_rel,
        'required_effect': mde_abs
    }