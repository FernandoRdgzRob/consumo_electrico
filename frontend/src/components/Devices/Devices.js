import React from 'react'
import { useQuery } from '@apollo/client'
import { GET_DEVICES_FROM_USER } from '../Queries/Queries'
import DevicesList from './DevicesList'

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
