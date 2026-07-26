import { BrowserRouter, Routes, Route } from 'react-router-dom';
import { AuthProvider } from './context/AuthContext';
import ProtectedRoute from './components/ProtectedRoute/ProtectedRoute';
import LandingPage from './pages/LandingPage';
import Login from './pages/auth/Login';
import Register from './pages/auth/Register';
import DashboardLayout from './layouts/DashboardLayout/DashboardLayout';
import Overview from './pages/dashboard/Overview';
import Platforms from './pages/dashboard/Platforms';
import PlatformDetail from './pages/dashboard/PlatformDetail';
import Revenue from './pages/dashboard/Revenue';
import Chat from './pages/dashboard/Chat';
import Settings from './pages/dashboard/Settings';
import Inbox from './pages/dashboard/Inbox';
import Scheduler from './pages/dashboard/Scheduler';

function App() {
  return (
    <BrowserRouter>
      <AuthProvider>
        <Routes>
          <Route path="/" element={<LandingPage />} />
          <Route path="/login" element={<Login />} />
          <Route path="/register" element={<Register />} />

          <Route
            path="/dashboard"
            element={
              <ProtectedRoute>
                <DashboardLayout />
              </ProtectedRoute>
            }
          >
            <Route index element={<Overview />} />
            <Route path="platforms" element={<Platforms />} />
            <Route path="platforms/:platform" element={<PlatformDetail />} />
            <Route path="inbox" element={<Inbox />} />
            <Route path="scheduler" element={<Scheduler />} />
            <Route path="revenue" element={<Revenue />} />
            <Route path="assistant" element={<Chat />} />
            <Route path="settings" element={<Settings />} />
          </Route>
        </Routes>
      </AuthProvider>
    </BrowserRouter>
  );
}

export default App;
