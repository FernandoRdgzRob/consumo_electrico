import { CssBaseline } from '@mui/material'
import { Routes, Route } from 'react-router-dom'
import Dashboard from './components/Dashboard/Dashboard'
import Devices from './components/Devices/Devices'
import ResponsiveDrawer from './components/Drawer/ResponsiveDrawer'
import Login from './components/Login/Login'
import PrivateRoute from './components/Routes/PrivateRoute'

function App () {
  return (
    <ResponsiveDrawer>
      <CssBaseline />
      <Routes>
        <Route path='/' element={<Login />} />
        <Route
          path='dashboard'
          element={
            <PrivateRoute>
              <Dashboard />
            </PrivateRoute>
          }
        />
        <Route
          path='dispositivos'
          element={
            <PrivateRoute>
              <Devices />
            </PrivateRoute>
          }
        />
      </Routes>
    </ResponsiveDrawer>
  )
}

export default App
