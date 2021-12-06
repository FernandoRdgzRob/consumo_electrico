import * as React from 'react'
// Material UI
import Box from '@mui/material/Box'
import Divider from '@mui/material/Divider'
import Drawer from '@mui/material/Drawer'
import IconButton from '@mui/material/IconButton'
import List from '@mui/material/List'
import ListItem from '@mui/material/ListItem'
import ListItemIcon from '@mui/material/ListItemIcon'
import ListItemText from '@mui/material/ListItemText'
import MenuIcon from '@mui/icons-material/Menu'
import Toolbar from '@mui/material/Toolbar'
import Typography from '@mui/material/Typography'
import HomeIcon from '@mui/icons-material/Home'
import DevicesIcon from '@mui/icons-material/Devices'
import PersonIcon from '@mui/icons-material/Person'
import { AppBar, Button } from '@mui/material'
import LogoutIcon from '@mui/icons-material/Logout'
// React Router
import { useLocation, useNavigate } from 'react-router-dom'

const drawerWidth = 240

const getTitle = (pathname, drawerItems) => {
  for (const [, value] of Object.entries(drawerItems)) {
    if (pathname === value.route) { return value.title }
  }
  return null
}

const ResponsiveDrawer = props => {
  const { window, children } = props
  const [mobileOpen, setMobileOpen] = React.useState(false)
  const location = useLocation()
  const navigate = useNavigate()

  const handleDrawerToggle = () => {
    setMobileOpen(!mobileOpen)
  }

  const logout = () => {
    localStorage.removeItem('token')
    navigate('/')
  }

  if (location.pathname === '/') {
    return children
  }

  const drawerItems = [
    {
      name: 'Inicio',
      route: '/dashboard',
      title: 'Resumen de consumo',
      icon: <HomeIcon />
    },
    {
      name: 'Dispositivos',
      route: '/dispositivos',
      title: 'Dispositivos agregados',
      icon: <DevicesIcon />
    }
  ]

  const drawer = (
    <div>
      {/* <Toolbar /> */}
      <div style={{ display: 'flex', justifyContent: 'center', marginTop: 10, marginBottom: 10 }}>
        <div>
          <div style={{ display: 'flex', justifyContent: 'center' }}>
            <PersonIcon sx={{ fontSize: 90 }} />
          </div>
        </div>
      </div>
      <Divider />
      <List>
        {drawerItems.map(item => {
          return (
            <ListItem
              selected={location.pathname === item.route}
              button
              key={item.name}
              onClick={() => navigate(item.route)}
            >
              <ListItemIcon>{item.icon}</ListItemIcon>
              <ListItemText primary={item.name} />
            </ListItem>
          )
        })}
      </List>
      <Divider />
      <List
        style={{
          display: 'flex',
          flexDirection: 'column',
          alignItems: 'center',
          justifyContent: 'flex-end',
          height: 450
        }}
      >
        <ListItem>
          <Button onClick={logout} fullWidth variant='outlined'>
            <ListItemIcon style={{ minWidth: 0, color: '#1976d2' }}><LogoutIcon /></ListItemIcon>
            <ListItemText primary='Cerrar sesión' />
          </Button>
        </ListItem>
      </List>
    </div>
  )

  const container = window !== undefined ? () => window().document.body : undefined

  const title = getTitle(location.pathname, drawerItems)

  return (
    <Box sx={{ display: 'flex' }}>
      <AppBar
        position='fixed'
        sx={{
          display: { xs: 'block', sm: 'none' },
          width: { sm: `calc(100% - ${drawerWidth}px)` },
          ml: { sm: `${drawerWidth}px` }
        }}
      >
        <Toolbar>
          <IconButton
            color='inherit'
            aria-label='open drawer'
            edge='start'
            onClick={handleDrawerToggle}
            sx={{ mr: 2, display: { sm: 'none' } }}
          >
            <MenuIcon />
          </IconButton>
          <Typography variant='h4' noWrap component='div'>
            {title}
          </Typography>
        </Toolbar>
      </AppBar>
      <Box
        component='nav'
        sx={{ width: { sm: drawerWidth }, flexShrink: { sm: 0 } }}
        aria-label='mailbox folders'
      >
        <Drawer
          container={container}
          variant='temporary'
          open={mobileOpen}
          onClose={handleDrawerToggle}
          ModalProps={{
            keepMounted: true // Better open performance on mobile.
          }}
          sx={{
            display: { xs: 'block', sm: 'none' },
            '& .MuiDrawer-paper': { boxSizing: 'border-box', width: drawerWidth }
          }}
        >
          {drawer}
        </Drawer>
        <Drawer
          variant='permanent'
          sx={{
            display: { xs: 'none', sm: 'block' },
            '& .MuiDrawer-paper': { boxSizing: 'border-box', width: drawerWidth }
          }}
          open
        >
          {drawer}
        </Drawer>
      </Box>
      <Box
        component='main'
        sx={{ flexGrow: 1, p: 4, width: { sm: `calc(100% - ${drawerWidth}px)` } }}
      >
        <Toolbar sx={{ display: { xs: 'block', sm: 'none' } }} />
        <Typography
          variant='h2'
          sx={{ display: { xs: 'none', sm: 'block' }, fontSize: 55, mb: 4 }}
        >
          {title}
        </Typography>
        {children}
      </Box>
    </Box>
  )
}

export default ResponsiveDrawer
