import axios from 'axios';

const API_URL = process.env.REACT_API_URL || 'http://localhost:5000';

const api = axios.create({
    baseURL: API_URL,
});

export const registerUser = (data) => api.post('/auth/register', data);
export const loginUser = async (data) => {
    try {
        const response = await api.post('/auth/login', data);
        return response.data; // Ensure this contains access_token and user_id
    } catch (error) {
        console.error('Error during login:', error);
        throw error.response ? error.response.data : new Error('Server Error');
    }
};
export const getUserName = (user_id) => api.get(`/contacts/username/${user_id}`);
export const addContact = (data) => api.post('/contacts/add', data);
export const markSpam = async ({ phone_number, user_id, isSpam }) => {
    return api.post('/spam/mark', { phone_number, user_id, isSpam });
};
export const listContacts = async (user_id, page = 1, per_page = 10) => {
    return api.get(`/contacts/list/${user_id}?page=${page}&per_page=${per_page}`);
};
export const searchByName = (query) => api.get(`/search/by_name?query=${query}`);
export const searchByPhone = (query) => api.get(`/search/by_phone?query=${query}`);
export const refreshToken = (data) => api.post('/refreshtoken', data);

export const verifyOtp = async (data) => {
    try {
        const response = await api.post('auth/verify', data);
        return response.data;
    } catch (error) {
        console.error('Error during OTP verification:', error);
        throw error.response ? error.response.data : new Error('Server Error');
    }
};


