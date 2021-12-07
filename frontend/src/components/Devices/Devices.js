import React from 'react'
import { useQuery } from '@apollo/client'
import { GET_DEVICES_FROM_USER } from '../Queries/Queries'
import DevicesList from './DevicesList'
import CircularProgress from '@mui/material/CircularProgress'

const Devices = () => {
  const { loading, error, data } = useQuery(GET_DEVICES_FROM_USER)

  if (loading) {
    return (
      <div style={{ display: 'flex', flex: 1, justifyContent: 'center', marginTop: 150 }}>
        <CircularProgress />
      </div>
    )
  }

  if (error) {
    console.log(error)
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
