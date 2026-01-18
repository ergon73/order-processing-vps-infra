-- SQL запрос для отображения всех важных столбцов в таблице applications
SELECT 
    id,
    first_name,
    last_name,
    middle_name,
    interested_product,  -- ← ВАЖНО: выбранная услуга
    budget,
    preferred_contact_method,
    comments,
    created_at
FROM public.applications
ORDER BY id DESC;
