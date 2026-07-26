import axiosInstance from '../services/axios';

export const getInboxMessages = async (platform = null, unreadOnly = false) => {
  const params = {};
  if (platform && platform !== 'all') params.platform = platform;
  if (unreadOnly) params.unread_only = true;
  
  const { data } = await axiosInstance.get('/inbox/messages', { params });
  return data.data;
};
