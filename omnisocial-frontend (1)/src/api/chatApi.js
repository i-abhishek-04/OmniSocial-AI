import axiosInstance from '../services/axios';

export const sendChatMessage = async (message) => {
  const { data } = await axiosInstance.post('/chat/messages', { message });
  return data.data.reply;
};

export const getChatHistory = async () => {
  const { data } = await axiosInstance.get('/chat/history');
  return data.data.messages;
};
