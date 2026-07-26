import axiosInstance from '../services/axios';

export const registerUser = async (payload) => {
  const { data } = await axiosInstance.post('/auth/register', payload);
  return data.data;
};

export const loginUser = async (payload) => {
  const { data } = await axiosInstance.post('/auth/login', payload);
  return data.data;
};

export const fetchMe = async () => {
  const { data } = await axiosInstance.get('/auth/me');
  return data.data;
};

export const updateProfile = async (payload) => {
  const { data } = await axiosInstance.put('/users/me', payload);
  return data.data;
};
