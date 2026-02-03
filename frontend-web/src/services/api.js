import axios from 'axios';

const API_BASE_URL = '/api';

const api = axios.create({
    baseURL: API_BASE_URL,
    headers: {
        'Content-Type': 'application/json',
    },
});

// Add auth token to requests
api.interceptors.request.use((config) => {
    const token = localStorage.getItem('token');
    if (token) {
        config.headers.Authorization = `Token ${token}`;
    }
    return config;
});

// Auth APIs
export const authAPI = {
    login: (username, password) =>
        api.post('/auth/login/', { username, password }),
    register: (username, password, email) =>
        api.post('/auth/register/', { username, password, email }),
    logout: () => api.post('/auth/logout/'),
    profile: () => api.get('/auth/profile/'),
};

// Dataset APIs
export const datasetAPI = {
    list: () => api.get('/datasets/'),
    get: (id) => api.get(`/datasets/${id}/`),
    upload: (file) => {
        const formData = new FormData();
        formData.append('file', file);
        return api.post('/datasets/', formData, {
            headers: { 'Content-Type': 'multipart/form-data' },
        });
    },
    getStats: (id) => api.get(`/datasets/${id}/stats/`),
    getEquipment: (id) => api.get(`/datasets/${id}/equipment/`),
    downloadReport: (id) =>
        api.get(`/datasets/${id}/report/`, { responseType: 'blob' }),
    delete: (id) => api.delete(`/datasets/${id}/`),
};

export default api;
