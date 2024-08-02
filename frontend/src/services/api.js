import axios from 'axios';

const API_URL = 'http://localhost:5000';

const api = axios.create({
    baseURL: API_URL,
});

export const registerUser = (data) => api.post('/auth/register', data);
export const verifyUser = (data) => api.post('/auth/verify', data);
export const loginUser = (data) => api.post('/auth/login', data);
export const addContact = (data) => api.post('/contacts/add', data);
export const listContacts = (userId) => api.get(`/contacts/list/${userId}`);
export const markSpam = (data) => api.post('/spam/mark', data);
export const searchByName = (query) => api.get(`/search/by_name?query=${query}`);
export const searchByPhone = (query) => api.get(`/search/by_phone?query=${query}`);
