import axiosInstance from '../services/axios';

export const getOverview = async () => {
  const { data } = await axiosInstance.get('/analytics/overview');
  return data.data;
};

export const getPlatforms = async () => {
  const { data } = await axiosInstance.get('/analytics/platforms');
  return data.data;
};

export const getPlatformDetail = async (platform) => {
  const { data } = await axiosInstance.get(`/analytics/platforms/${platform}`);
  return data.data;
};

export const connectPlatform = async (platform, handle) => {
  const { data } = await axiosInstance.post(`/analytics/platforms/${platform}/connect`, { handle });
  return data.data;
};

export const disconnectPlatform = async (platform) => {
  const { data } = await axiosInstance.post(`/analytics/platforms/${platform}/disconnect`);
  return data.data;
};

export const getRevenue = async () => {
  const { data } = await axiosInstance.get('/analytics/revenue');
  return data.data;
};
