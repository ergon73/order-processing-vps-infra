-- Обновление priority_score для существующих заявок
-- Использует алгоритм из core/priority.py

UPDATE applications 
SET priority_score = 
    -- Бюджет (40%)
    CASE 
        WHEN budget::text LIKE '%5000000%' OR budget::text LIKE '%10000000%' OR budget::text LIKE '%5m%' OR budget::text LIKE '%10m%' THEN 40
        WHEN budget::text LIKE '%1000000%' OR budget::text LIKE '%1m%' THEN 30
        WHEN budget::text LIKE '%500000%' OR budget::text LIKE '%500k%' THEN 20
        ELSE 10
    END +
    -- Размер компании (30%)
    CASE 
        WHEN company_size LIKE '%500+%' OR company_size LIKE '%500%' THEN 30
        WHEN company_size LIKE '%100-500%' OR company_size LIKE '%100%' THEN 20
        WHEN company_size LIKE '%50-100%' OR company_size LIKE '%50%' THEN 15
        ELSE 5
    END +
    -- Срочность (30%)
    CASE 
        WHEN deadline LIKE '%неделя%' OR deadline LIKE '%week%' OR comments LIKE '%срочно%' OR comments LIKE '%urgent%' THEN 30
        WHEN deadline LIKE '%месяц%' OR deadline LIKE '%month%' THEN 15
        ELSE 5
    END
WHERE priority_score = 0 OR priority_score IS NULL;

-- Проверка результата
SELECT id, first_name, budget, company_size, deadline, priority_score 
FROM applications 
ORDER BY priority_score DESC;
