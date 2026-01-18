import './styles.css';

const API_BASE = '/api';

// Load services on page load
document.addEventListener('DOMContentLoaded', async () => {
    const select = document.getElementById('service-select');
    
    try {
        // Load all services directly (more reliable than /latest/)
        const response = await fetch(`${API_BASE}/admin-settings/`);
        
        if (!response.ok) {
            throw new Error(`HTTP ${response.status}`);
        }
        
        const data = await response.json();
        
        if (Array.isArray(data) && data.length > 0) {
            select.innerHTML = '<option value="">Выберите услугу</option>';
            data.forEach(item => {
                if (item.services) {
                    const option = document.createElement('option');
                    option.value = item.services;
                    option.textContent = `${item.services} (${item.budget_range || ''})`;
                    select.appendChild(option);
                }
            });
        } else {
            select.innerHTML = '<option value="">Услуги не найдены</option>';
        }
    } catch (error) {
        console.error('Error loading services:', error);
        select.innerHTML = '<option value="">Ошибка загрузки услуг</option>';
    }
});

// Handle form submission
document.getElementById('application-form').addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const formData = new FormData(e.target);
    const data = Object.fromEntries(formData.entries());
    
    // Add selected service
    data.interested_product = document.getElementById('service-select').value;
    
    const messageDiv = document.getElementById('message');
    messageDiv.textContent = '';
    messageDiv.className = 'message';
    
    try {
        // CRITICAL: Use trailing slash to avoid 307 redirect
        const response = await fetch(`${API_BASE}/applications/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        });
        
        if (response.ok) {
            messageDiv.textContent = 'Заявка отправлена! Мы свяжемся с вами в ближайшее время.';
            messageDiv.classList.add('success');
            e.target.reset();
        } else {
            throw new Error(`HTTP ${response.status}`);
        }
    } catch (error) {
        console.error('Error submitting application:', error);
        messageDiv.textContent = 'Ошибка отправки заявки. Попробуйте позже.';
        messageDiv.classList.add('error');
    }
});
