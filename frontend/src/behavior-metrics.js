// Сбор поведенческих метрик на главной странице
const API_BASE = '/api';

let timeOnPage = 0;
let cursorPositions = [];
let buttonsClicked = {};

// Таймер для времени на странице (каждую секунду)
setInterval(() => {
    timeOnPage++;
}, 1000);

// Сбор координат курсора
document.addEventListener('mousemove', (e) => {
    cursorPositions.push({ x: e.clientX, y: e.clientY });
});

// Сбор кликов по элементам
document.addEventListener('click', (e) => {
    const target = e.target.id || e.target.className || e.target.tagName || 'unknown';
    buttonsClicked[target] = (buttonsClicked[target] || 0) + 1;
});

// Отправка метрик каждую секунду
setInterval(async () => {
    try {
        await fetch(`${API_BASE}/behavior-metrics/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                application_id: 0,  // Для анонимных метрик
                time_on_page: timeOnPage,
                buttons_clicked: JSON.stringify(buttonsClicked),
                cursor_positions: JSON.stringify(cursorPositions),
                return_frequency: 0
            })
        });
        
        // Очистка массива координат после отправки (чтобы не раздувался)
        cursorPositions = [];
    } catch (error) {
        // Тихо игнорируем ошибки, чтобы не мешать пользователю
        console.debug('Metrics send error (silent):', error);
    }
}, 1000);
