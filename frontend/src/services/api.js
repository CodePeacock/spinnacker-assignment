import axios from 'axios';

// Create an Axios instance
const api = axios.create({
    baseURL: process.env.REACT_APP_API_URL || 'http://localhost:5000',
});

// Add a request interceptor
api.interceptors.request.use(request => {
    console.log('Sending request:', request);
    return request;
}, error => {
    console.error('Error in request:', error);
    return Promise.reject(error);
});

// Function to register a user
export const registerUser = (data) => {
    console.log('registerUser called with data:', data);
    return api.post('/auth/register', data);
};

export const loginUser = async (data) => {
    console.log('loginUser called with data:', data);
    try {
        const response = await api.post('/auth/login', data);
        console.log('loginUser response:', response);
        return response.data; // Ensure this contains access_token and user_id
    } catch (error) {
        console.error('Error during login:', error);
        throw error.response ? error.response.data : new Error('Server Error');
    }
};

export const getUserName = (user_id) => {
    console.log('getUserName called with user_id:', user_id);
    return api.get(`/contacts/username/${user_id}`);
};

export const addContact = (data) => {
    console.log('addContact called with data:', data);
    return api.post('/contacts/add', data);
};

export const markSpam = async ({ phone_number, user_id, isSpam }) => {
    console.log('markSpam called with:', { phone_number, user_id, isSpam });
    return api.post('/spam/mark', { phone_number, user_id, isSpam });
};

export const listContacts = async (user_id, page = 1, per_page = 10) => {
    console.log('listContacts called with:', { user_id, page, per_page });
    return api.get(`/contacts/list/${user_id}?page=${page}&per_page=${per_page}`);
};

export const searchByName = (query) => {
    console.log('searchByName called with query:', query);
    return api.get(`/search/by_name?query=${query}`);
};

export const searchByPhone = (query) => {
    console.log('searchByPhone called with query:', query);
    return api.get(`/search/by_phone?query=${query}`);
};

export const refreshToken = (data) => {
    console.log('refreshToken called with data:', data);
    return api.post('/refreshtoken', data);
};

export const verifyOtp = async (data) => {
    console.log('verifyOtp called with data:', data);
    try {
        const response = await api.post('auth/verify', data);
        console.log('verifyOtp response:', response);
        return response.data;
    } catch (error) {
        console.error('Error during OTP verification:', error);
        throw error.response ? error.response.data : new Error('Server Error');
    }
};


