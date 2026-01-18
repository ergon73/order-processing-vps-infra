const API_BASE = '/api';

// Проверка наличия админов при загрузке страницы
document.addEventListener('DOMContentLoaded', async () => {
    try {
        const response = await fetch(`${API_BASE}/auth/check`);
        const data = await response.json();
        
        const registerSection = document.getElementById('register-section');
        const loginSection = document.getElementById('login-section');
        
        if (data.admin_exists) {
            // Админы есть - показываем только форму входа
            registerSection.style.display = 'none';
        } else {
            // Админов нет - показываем форму регистрации
            registerSection.style.display = 'block';
        }
    } catch (error) {
        console.error('Error checking admin status:', error);
        document.getElementById('register-message').textContent = 'Ошибка проверки статуса админов';
    }
});

// Регистрация первого админа
const registerForm = document.getElementById('register-form');
if (registerForm) {
    registerForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        
        const email = document.getElementById('register-email').value;
        const password = document.getElementById('register-password').value;
        const passwordConfirm = document.getElementById('register-password-confirm').value;
        const messageDiv = document.getElementById('register-message');
        
        if (password !== passwordConfirm) {
            messageDiv.textContent = 'Пароли не совпадают';
            messageDiv.style.color = 'red';
            return;
        }
        
        try {
            const response = await fetch(`${API_BASE}/auth/register`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ email, password }),
            });
            
            if (response.ok) {
                const data = await response.json();
                messageDiv.textContent = 'Регистрация успешна! Теперь вы можете войти.';
                messageDiv.style.color = 'green';
                
                // Скрываем форму регистрации после успешной регистрации
                document.getElementById('register-section').style.display = 'none';
            } else {
                const error = await response.json();
                messageDiv.textContent = error.detail || 'Ошибка регистрации';
                messageDiv.style.color = 'red';
            }
        } catch (error) {
            console.error('Registration error:', error);
            messageDiv.textContent = 'Ошибка регистрации';
            messageDiv.style.color = 'red';
        }
    });
}

// Вход в систему
const loginForm = document.getElementById('login-form');
if (loginForm) {
    loginForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        
        const email = document.getElementById('login-email').value;
        const password = document.getElementById('login-password').value;
        const messageDiv = document.getElementById('login-message');
        
        try {
            // FastAPI OAuth2PasswordRequestForm использует form-data, не JSON
            const formData = new URLSearchParams();
            formData.append('username', email);  // OAuth2 использует username, а не email
            formData.append('password', password);
            
            const response = await fetch(`${API_BASE}/auth/login`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded',
                },
                body: formData,
            });
            
            if (response.ok) {
                const data = await response.json();
                // Сохраняем токен в localStorage
                localStorage.setItem('access_token', data.access_token);
                messageDiv.textContent = 'Вход успешен! Перенаправление...';
                messageDiv.style.color = 'green';
                
                // Перенаправление на админ-панель
                setTimeout(() => {
                    window.location.href = '/admin.html';
                }, 1000);
            } else {
                const error = await response.json();
                messageDiv.textContent = error.detail || 'Ошибка входа';
                messageDiv.style.color = 'red';
            }
        } catch (error) {
            console.error('Login error:', error);
            messageDiv.textContent = 'Ошибка входа';
            messageDiv.style.color = 'red';
        }
    });
}

// Функция получения токена (для использования в других скриптах)
export function getAccessToken() {
    return localStorage.getItem('access_token');
}

// Функция проверки авторизации
export function isAuthenticated() {
    return !!localStorage.getItem('access_token');
}

// Функция выхода
export function logout() {
    localStorage.removeItem('access_token');
    window.location.href = '/login.html';
}
