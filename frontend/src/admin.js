import { getAccessToken, isAuthenticated, logout } from './auth.js';

const API_BASE = '/api';

// Проверка авторизации при загрузке
if (!isAuthenticated()) {
    window.location.href = '/login.html';
}

// Защищенный fetch с JWT токеном
async function authFetch(url, options = {}) {
    const token = getAccessToken();
    if (!token) {
        window.location.href = '/login.html';
        return;
    }
    
    const headers = {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`,
        ...options.headers
    };
    
    const response = await fetch(url, { ...options, headers });
    
    if (response.status === 401) {
        // Токен истек - перенаправление на логин
        logout();
        return response;
    }
    
    return response;
}

// ========== Управление вкладками ==========
document.addEventListener('DOMContentLoaded', () => {
    // Табы
    const tabs = document.querySelectorAll('.tab');
    const tabContents = document.querySelectorAll('.tab-content');
    
    tabs.forEach(tab => {
        tab.addEventListener('click', () => {
            const targetTab = tab.dataset.tab;
            
            tabs.forEach(t => t.classList.remove('active'));
            tabContents.forEach(tc => tc.classList.remove('active'));
            
            tab.classList.add('active');
            document.getElementById(`${targetTab}-tab`).classList.add('active');
            
            // Загружаем данные при переключении вкладок
            if (targetTab === 'services') {
                loadServices();
            } else if (targetTab === 'applications') {
                loadApplications();
            } else if (targetTab === 'statistics') {
                loadStatistics();
            }
        });
    });
    
    // Выход
    document.getElementById('logout-btn').addEventListener('click', () => {
        logout();
    });
    
    // Инициализация
    loadServices();
    setupServiceModal();
    setupApplicationModal();
});

// ========== Услуги (CRUD) ==========
async function loadServices() {
    try {
        const response = await fetch(`${API_BASE}/admin-settings/`);
        if (!response.ok) throw new Error('Failed to load services');
        
        const services = await response.json();
        const tbody = document.getElementById('services-tbody');
        tbody.innerHTML = '';
        
        services.forEach(service => {
            const tr = document.createElement('tr');
            tr.innerHTML = `
                <td>${service.id}</td>
                <td>${service.services || ''}</td>
                <td>${service.budget_range || ''}</td>
                <td>
                    <button class="btn btn-primary" onclick="editService(${service.id}, '${(service.services || '').replace(/'/g, "\\'")}', '${(service.budget_range || '').replace(/'/g, "\\'")}')">Редактировать</button>
                    <button class="btn btn-danger" onclick="deleteService(${service.id})">Удалить</button>
                </td>
            `;
            tbody.appendChild(tr);
        });
    } catch (error) {
        console.error('Error loading services:', error);
        alert('Ошибка загрузки услуг');
    }
}

function setupServiceModal() {
    const modal = document.getElementById('service-modal');
    const closeBtn = document.getElementById('close-modal');
    const addBtn = document.getElementById('add-service-btn');
    const form = document.getElementById('service-form');
    
    addBtn.addEventListener('click', () => {
        document.getElementById('modal-title').textContent = 'Добавить услугу';
        document.getElementById('service-id').value = '';
        document.getElementById('service-name').value = '';
        document.getElementById('service-budget').value = '';
        modal.style.display = 'block';
    });
    
    closeBtn.addEventListener('click', () => {
        modal.style.display = 'none';
    });
    
    form.addEventListener('submit', async (e) => {
        e.preventDefault();
        
        const id = document.getElementById('service-id').value;
        const name = document.getElementById('service-name').value;
        const budget = document.getElementById('service-budget').value;
        
        try {
            if (id) {
                // Обновление
                await authFetch(`${API_BASE}/admin-settings/${id}`, {
                    method: 'PUT',
                    body: JSON.stringify({
                        services: name,
                        budget_range: budget
                    })
                });
            } else {
                // Создание
                await authFetch(`${API_BASE}/admin-settings/`, {
                    method: 'POST',
                    body: JSON.stringify({
                        services: name,
                        budget_range: budget
                    })
                });
            }
            
            modal.style.display = 'none';
            loadServices();
        } catch (error) {
            console.error('Error saving service:', error);
            alert('Ошибка сохранения услуги');
        }
    });
}

window.editService = function(id, name, budget) {
    document.getElementById('modal-title').textContent = 'Редактировать услугу';
    document.getElementById('service-id').value = id;
    document.getElementById('service-name').value = name;
    document.getElementById('service-budget').value = budget;
    document.getElementById('service-modal').style.display = 'block';
};

window.deleteService = async function(id) {
    if (!confirm('Вы уверены, что хотите удалить эту услугу?')) return;
    
    try {
        await authFetch(`${API_BASE}/admin-settings/${id}`, {
            method: 'DELETE'
        });
        loadServices();
    } catch (error) {
        console.error('Error deleting service:', error);
        alert('Ошибка удаления услуги');
    }
};

// ========== Заявки ==========
async function loadApplications() {
    try {
        const response = await authFetch(`${API_BASE}/applications/`);
        if (!response || !response.ok) throw new Error('Failed to load applications');
        
        const applications = await response.json();
        const tbody = document.getElementById('applications-tbody');
        tbody.innerHTML = '';
        
        applications.forEach(app => {
            const tr = document.createElement('tr');
            const priorityClass = getPriorityClass(app.priority_score || 0);
            const priorityEmoji = getPriorityEmoji(app.priority_score || 0);
            
            tr.className = priorityClass;
            tr.innerHTML = `
                <td>${app.id}</td>
                <td>${app.first_name || ''} ${app.last_name || ''}</td>
                <td>${app.interested_product || '-'}</td>
                <td>${app.budget || '-'}</td>
                <td>${priorityEmoji} ${app.priority_score || 0}</td>
                <td>
                    <button class="btn btn-primary" onclick="viewApplication(${app.id})">Просмотр</button>
                </td>
            `;
            tbody.appendChild(tr);
        });
    } catch (error) {
        console.error('Error loading applications:', error);
        alert('Ошибка загрузки заявок');
    }
}

function getPriorityClass(score) {
    if (score > 80) return 'priority-high';
    if (score >= 50) return 'priority-medium';
    return 'priority-low';
}

function getPriorityEmoji(score) {
    if (score > 80) return '🔥';
    if (score >= 50) return '⚠️';
    return '✅';
}

function setupApplicationModal() {
    const modal = document.getElementById('application-modal');
    const closeBtn = document.getElementById('close-app-modal');
    
    closeBtn.addEventListener('click', () => {
        modal.style.display = 'none';
    });
}

window.viewApplication = async function(id) {
    try {
        const response = await authFetch(`${API_BASE}/applications/${id}`);
        if (!response || !response.ok) throw new Error('Failed to load application');
        
        const app = await response.json();
        const detailsDiv = document.getElementById('application-details');
        
        detailsDiv.innerHTML = `
            <p><strong>ID:</strong> ${app.id}</p>
            <p><strong>Имя:</strong> ${app.first_name || '-'}</p>
            <p><strong>Фамилия:</strong> ${app.last_name || '-'}</p>
            <p><strong>Отчество:</strong> ${app.middle_name || '-'}</p>
            <p><strong>Услуга:</strong> ${app.interested_product || '-'}</p>
            <p><strong>Бюджет:</strong> ${app.budget || '-'}</p>
            <p><strong>Размер компании:</strong> ${app.company_size || '-'}</p>
            <p><strong>Срок:</strong> ${app.deadline || '-'}</p>
            <p><strong>Бизнес-информация:</strong> ${app.business_info || '-'}</p>
            <p><strong>Комментарии:</strong> ${app.comments || '-'}</p>
            <p><strong>Приоритет (score):</strong> ${getPriorityEmoji(app.priority_score || 0)} ${app.priority_score || 0}</p>
            <p><strong>Создано:</strong> ${new Date(app.created_at).toLocaleString('ru-RU')}</p>
        `;
        
        document.getElementById('application-modal').style.display = 'block';
    } catch (error) {
        console.error('Error loading application:', error);
        alert('Ошибка загрузки заявки');
    }
};

// ========== Статистика ==========
async function loadStatistics() {
    try {
        const response = await authFetch(`${API_BASE}/behavior-metrics/stats`);
        if (!response || !response.ok) throw new Error('Failed to load statistics');
        
        const stats = await response.json();
        
        document.getElementById('avg-day').textContent = Math.round(stats.average_time_on_page.day || 0);
        document.getElementById('avg-week').textContent = Math.round(stats.average_time_on_page.week || 0);
        document.getElementById('avg-month').textContent = Math.round(stats.average_time_on_page.month || 0);
        
        // Отрисовка heatmap
        drawHeatmap(stats.heatmap_coordinates || []);
    } catch (error) {
        console.error('Error loading statistics:', error);
        document.getElementById('stats-content').innerHTML = '<p>Ошибка загрузки статистики</p>';
    }
}

function drawHeatmap(coordinates) {
    const canvas = document.getElementById('heatmap-canvas');
    if (!canvas) return;
    
    const ctx = canvas.getContext('2d');
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    
    if (coordinates.length === 0) {
        ctx.font = '16px Arial';
        ctx.fillStyle = '#666';
        ctx.fillText('Нет данных для heatmap', 10, 30);
        return;
    }
    
    // Фильтруем валидные координаты (в пределах разумных значений)
    const validCoords = coordinates.filter(coord => 
        coord && typeof coord.x === 'number' && typeof coord.y === 'number' &&
        coord.x >= 0 && coord.y >= 0 && coord.x < 10000 && coord.y < 10000
    );
    
    if (validCoords.length === 0) {
        ctx.font = '16px Arial';
        ctx.fillStyle = '#666';
        ctx.fillText('Нет валидных координат для heatmap', 10, 30);
        return;
    }
    
    // Находим границы координат для масштабирования
    const minX = Math.min(...validCoords.map(c => c.x));
    const maxX = Math.max(...validCoords.map(c => c.x));
    const minY = Math.min(...validCoords.map(c => c.y));
    const maxY = Math.max(...validCoords.map(c => c.y));
    
    // Масштабируем под размер canvas с отступами
    const padding = 20;
    const scaleX = (canvas.width - padding * 2) / Math.max(maxX - minX, 1);
    const scaleY = (canvas.height - padding * 2) / Math.max(maxY - minY, 1);
    const scale = Math.min(scaleX, scaleY); // Используем меньший масштаб для сохранения пропорций
    
    // Агрегация координат (подсчет частоты) с учетом масштабирования
    const coordMap = {};
    validCoords.forEach(coord => {
        const scaledX = Math.floor((coord.x - minX) * scale + padding);
        const scaledY = Math.floor((coord.y - minY) * scale + padding);
        const key = `${scaledX},${scaledY}`;
        coordMap[key] = (coordMap[key] || 0) + 1;
    });
    
    // Находим максимальную частоту для нормализации
    const maxFreq = Math.max(...Object.values(coordMap));
    
    // Отрисовка точек (градиент от синего к красному)
    Object.entries(coordMap).forEach(([key, freq]) => {
        const [x, y] = key.split(',').map(Number);
        const intensity = freq / maxFreq;
        
        // Градиент: синий (холодный) → красный (горячий)
        const r = Math.floor(intensity * 255);
        const b = Math.floor((1 - intensity) * 255);
        
        ctx.fillStyle = `rgb(${r}, 0, ${b})`;
        ctx.beginPath();
        // Размер точки зависит от частоты
        const radius = 2 + Math.floor(intensity * 4);
        ctx.arc(x, y, radius, 0, Math.PI * 2);
        ctx.fill();
    });
    
    // Добавляем информацию о количестве точек
    ctx.font = '12px Arial';
    ctx.fillStyle = '#333';
    ctx.fillText(`Всего точек: ${validCoords.length}`, 10, canvas.height - 10);
}
