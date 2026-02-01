import axios from 'axios';

const API_URL = 'http://localhost:8000/api';

export const submitPredictionRequest = async (data) => {
    return await axios.post(`${API_URL}/predict`, data);
};

export const checkRequestStatus = async (requestId) => {
    return await axios.get(`${API_URL}/status/${requestId}`);
};

export const submitFeedback = async (data) => {
    return await axios.post(`${API_URL}/feedback`, data);
};
