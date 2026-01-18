"""
Алгоритм приоритизации заявок на основе бюджета, размера компании и срочности.
"""

def calculate_priority_score(application) -> int:
    """
    Вычисляет score (оценку) заявки на основе трех критериев:
    - Бюджет (40% веса)
    - Размер компании (30% веса)
    - Срочность (30% веса)
    
    Возвращает: score (0-100)
    """
    score = 0
    budget = (application.budget or "").lower()
    company_size = (application.company_size or "").lower()
    deadline = (application.deadline or "").lower()
    comments = (application.comments or "").lower()
    
    # Бюджет (вес 40%)
    # Пытаемся извлечь числовое значение бюджета
    budget_num = None
    try:
        # Убираем все нецифровые символы, кроме дефисов и пробелов
        budget_clean = ''.join(c for c in budget if c.isdigit() or c in '- ')
        # Пытаемся найти диапазон (например, "500000-1000000")
        if '-' in budget_clean:
            parts = budget_clean.split('-')
            if len(parts) == 2:
                budget_num = max(int(parts[0].strip()), int(parts[1].strip()))
        else:
            # Одно число
            budget_num = int(budget_clean.strip())
    except (ValueError, AttributeError):
        pass
    
    if budget_num:
        if budget_num >= 5000000:
            score += 40
        elif budget_num >= 1000000:
            score += 30
        elif budget_num >= 500000:
            score += 20
        else:
            score += 10
    else:
        # Fallback на строковую проверку для форматов типа "5m", "500k"
        if '5000000' in budget or '5m' in budget or '10000000' in budget or '10m' in budget:
            score += 40
        elif '1000000' in budget or '1m' in budget:
            score += 30
        elif '500000' in budget or '500k' in budget:
            score += 20
        else:
            score += 10
    
    # Размер компании (вес 30%)
    if '500+' in company_size or '500' in company_size:
        score += 30
    elif '100-500' in company_size or '100' in company_size:
        score += 20
    elif '50-100' in company_size or '50' in company_size:
        score += 15
    else:
        score += 5
    
    # Срочность (вес 30%)
    # Проверяем наличие слов "неделя", "недел", "week" или "срочно"
    if 'недел' in deadline or 'срочно' in comments or 'week' in deadline:
        score += 30
    elif 'месяц' in deadline or 'month' in deadline:
        score += 15
    else:
        score += 5
    
    return score
