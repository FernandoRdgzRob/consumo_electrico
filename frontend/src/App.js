import { CssBaseline } from '@mui/material'
import { Routes, Route } from 'react-router-dom'
import Dashboard from './components/Dashboard/Dashboard'
import Devices from './components/Devices/Devices'
// import CustomChart from './components/Chart/Chart'
// import Devices from './components/Devices/Devices'
import ResponsiveDrawer from './components/Drawer/ResponsiveDrawer'
import Login from './components/Login/Login'
import DateAdapter from '@mui/lab/AdapterDateFns'

function App () {
  return (
    <ResponsiveDrawer>
      <CssBaseline />
      <Routes>
        <Route path='/' element={<Login />} />
        <Route path='dashboard' element={<Dashboard />} />
        <Route path='dispositivos' element={<Devices />} />
      </Routes>
    </ResponsiveDrawer>
  )
}

export default App
