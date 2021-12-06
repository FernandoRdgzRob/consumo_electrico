import React from 'react'
import { useQuery } from '@apollo/client'
import { GET_DEVICES_FROM_USER } from '../Queries/Queries'
import {
  Button,
  Card,
  CardActions,
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
      <Grid container spacing={3} columns={14}>
        {devices.map((device, index) => {
          const creationDate = new Date(device.creation_date)
          creationDate.setTime(creationDate.getTime() + creationDate.getTimezoneOffset() * 60 * 1000)
          return (
            <Grid key={index} item xs={3}>
              <Card sx={{ width: '100%' }}>
                <CardContent>
                  <Typography variant='h5'>{device.name}</Typography>
                  <Typography variant='body2'>Añadido el {format(new Date(creationDate), 'dd/MM/yyyy')}</Typography>
                  <DeviceImage name={device.name} />
                </CardContent>
                <CardActions sx={{ display: 'flex', justifyContent: 'flex-end' }}>
                  <Button variant='outlined' color='error' size='small'>
                    Eliminar dispositivo
                  </Button>
                </CardActions>
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

const Devices = () => {
  const { loading, error, data } = useQuery(GET_DEVICES_FROM_USER)

  if (loading) {
    return (
      <div>
        Cargando...
      </div>
    )
  }
  if (error) {
    console.log({ error })
  }

  let devices = []
  if (data) {
    devices = data?.getDevicesFromUser?.devices
  }

  return (
    <DevicesList devices={devices} />
  )
}

export default Devices
