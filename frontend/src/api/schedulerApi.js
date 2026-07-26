import axiosInstance from '../services/axios';

export const getScheduledPosts = async () => {
  const { data } = await axiosInstance.get('/scheduler/posts');
  return data.data;
};

export const createScheduledPost = async (postData) => {
  const { data } = await axiosInstance.post('/scheduler/posts', postData);
  return data.data;
};

export const updateScheduledPost = async (postId, postData) => {
  const { data } = await axiosInstance.put(`/scheduler/posts/${postId}`, postData);
  return data.data;
};

export const deleteScheduledPost = async (postId) => {
  const { data } = await axiosInstance.delete(`/scheduler/posts/${postId}`);
  return data.data;
};

export const getBestTimeRecommendations = async () => {
  const { data } = await axiosInstance.get('/scheduler/recommendations');
  return data.data;
};
