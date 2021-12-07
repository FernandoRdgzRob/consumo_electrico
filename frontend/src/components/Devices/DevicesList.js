import React from 'react'
import {
  Card,
  CardContent,
  Grid,
  Typography
} from '@mui/material'
import { format } from 'date-fns'
import DeviceImage from './DeviceImage'
import AddCircleIcon from '@mui/icons-material/AddCircle'
import UpsertDeviceModal from './UpsertDeviceModal'

const DevicesList = ({ devices }) => {
  const [open, setOpen] = React.useState(false)

  const handleClickOpen = () => {
    setOpen(true)
  }

  return (
    <>
      <UpsertDeviceModal open={open} setOpen={setOpen} />
      <Grid container spacing={3}>
        {devices.map((device, index) => {
          const creationDate = new Date(device.creation_date)
          creationDate.setTime(creationDate.getTime() + creationDate.getTimezoneOffset() * 60 * 1000)
          return (
            <Grid key={index} item xs={3}>
              <Card sx={{ minHeight: 210, width: '100%' }}>
                <CardContent>
                  <Typography sx={{ mt: 1 }} variant='h5'>{device.name}</Typography>
                  <Typography sx={{ mb: 2 }} variant='body2'>Añadido el {format(new Date(creationDate), 'dd/MM/yyyy')}</Typography>
                  <DeviceImage name={device.type} />
                </CardContent>
              </Card>
            </Grid>
          )
        })}
        <Grid item xs={3}>
          <div style={{ cursor: 'pointer' }} onClick={handleClickOpen}>
            <Card sx={{ width: '100%' }}>
              <CardContent sx={{ height: 220.383 }}>
                <div style={{ display: 'flex', justifyContent: 'center' }}>
                  <Typography sx={{ textAlign: 'center', mt: 1, mb: 1 }} variant='h5'>
                    Agregar dispositivo
                  </Typography>
                </div>
                <div style={{ display: 'flex', justifyContent: 'center' }}>
                  <AddCircleIcon sx={{ color: 'black', fontSize: 90 }} />
                </div>
              </CardContent>
            </Card>
          </div>
        </Grid>
      </Grid>
    </>
  )
}
export default DevicesList
