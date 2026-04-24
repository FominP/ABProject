import pytest
import numpy as np
from ab_test_analyzer.core import (
    ztest_proportions,
    ttest_means,
    chi_square_test,
    check_srm,
    calculate_mde,
)

# Фиксируем random seed для воспроизводимости
np.random.seed(42)

# Уровень значимости
ALPHA = 0.05
# Количество итераций
N_ITER = 10000
# Ожидаемая доля отвержений в А/А
EXPECTED_REJECTION_RATE = ALPHA
# Допустимые границы (при N_ITER=1000, 95% доверительный интервал для 0.05: ~0.036..0.064)
LOWER_BOUND = 0.04
UPPER_BOUND = 0.06

# -------------------- Z-тест (пропорции) --------------------
def test_ztest_aa():
    """А/А тест: две одинаковые группы, p-value должен быть >0.05 в ~95% случаев"""
    rejections = 0
    for _ in range(N_ITER):
        # Генерируем две выборки с одинаковой конверсией 0.1
        n = 1000
        p = 0.1
        conv1 = np.random.binomial(n, p)
        conv2 = np.random.binomial(n, p)
        res = ztest_proportions(conv1, n, conv2, n)
        if res['p_value'] < ALPHA:
            rejections += 1
    observed_rate = rejections / N_ITER
    assert LOWER_BOUND < observed_rate < UPPER_BOUND, f"Z-test A/A: observed {observed_rate:.3f}"

def test_ztest_ab():
    """А/Б тест: группы с разными конверсиями (эффект ~20% относительный)"""
    rejections = 0
    n = 1000
    p_control = 0.1
    p_test = 0.13
    for _ in range(N_ITER):
        conv_control = np.random.binomial(n, p_control)
        conv_test = np.random.binomial(n, p_test)
        res = ztest_proportions(conv_control, n, conv_test, n)
        if res['p_value'] < ALPHA:
            rejections += 1
    power = rejections / N_ITER
    # Ожидаемая мощность при таком эффекте > 0.9
    assert power > 0.8, f"Z-test A/B мощность = {power:.3f} (ожидаем > 0.8)"

# -------------------- T-тест (средние) --------------------
def test_ttest_aa():
    """А/А тест для средних (нормальные данные)"""
    rejections = 0
    n = 100
    mean_common = 10.0
    std_common = 2.0
    for _ in range(N_ITER):
        control = np.random.normal(mean_common, std_common, n)
        test = np.random.normal(mean_common, std_common, n)
        mean_c = np.mean(control)
        mean_t = np.mean(test)
        std_c = np.std(control, ddof=1)
        std_t = np.std(test, ddof=1)
        res = ttest_means(mean_c, mean_t, std_c, std_t, n, n)
        if res['p_value'] < ALPHA:
            rejections += 1
    observed_rate = rejections / N_ITER
    assert LOWER_BOUND < observed_rate < UPPER_BOUND, f"T-test A/A: observed {observed_rate:.3f}"

def test_ttest_ab():
    rejections = 0
    n = 100
    mean_control = 10.0
    mean_test = 11.0
    std = 2.0
    for _ in range(N_ITER):
        control = np.random.normal(mean_control, std, n)
        test = np.random.normal(mean_test, std, n)
        mean_c = np.mean(control)
        mean_t = np.mean(test)
        std_c = np.std(control, ddof=1)
        std_t = np.std(test, ddof=1)
        res = ttest_means(mean_c, mean_t, std_c, std_t, n, n)
        if res['p_value'] < ALPHA:
            rejections += 1
    power = rejections / N_ITER
    assert power > 0.8, f"T-test A/B мощность = {power:.3f} (ожидаем > 0.8)"

# -------------------- Хи-квадрат тест (таблица 2x2) --------------------
def test_chisquare_aa():
    """А/А: две одинаковые группы, таблица 2x2"""
    rejections = 0
    n = 1000
    p = 0.1
    for _ in range(N_ITER):
        a = np.random.binomial(n, p)
        c = n - a
        b = np.random.binomial(n, p)
        d = n - b
        res = chi_square_test([a, b, c, d])
        if res['p_value'] < ALPHA:
            rejections += 1
    observed_rate = rejections / N_ITER
    assert LOWER_BOUND < observed_rate < UPPER_BOUND, f"Chi2 A/A: observed {observed_rate:.3f}"

def test_chisquare_ab():
    rejections = 0
    n = 1000
    p_control = 0.1
    p_test = 0.13
    for _ in range(N_ITER):
        a = np.random.binomial(n, p_control)
        b = np.random.binomial(n, p_test)
        c = n - a
        d = n - b
        res = chi_square_test([a, b, c, d])
        if res['p_value'] < ALPHA:
            rejections += 1
    power = rejections / N_ITER
    assert power > 0.8, f"Chi2 A/B мощность = {power:.3f} (ожидаем > 0.8)"

# -------------------- SRM --------------------
def test_srm():
    # 1010 и 990 дают χ² = 0.2, p-value ≈ 0.65
    res = check_srm(1010, 990)
    assert res['p_value'] > 0.05, f"SRM p-value = {res['p_value']} (ожидаем > 0.05)"

# -------------------- MDE --------------------
def test_mde():
    res = calculate_mde(baseline_conversion=0.1, n_control=1000)
    assert 0.02 < res['mde_absolute'] < 0.05, f"MDE = {res['mde_absolute']} вне (0.02, 0.05)"