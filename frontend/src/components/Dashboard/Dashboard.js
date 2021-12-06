import { useQuery } from '@apollo/client'
import { format } from 'date-fns'
import React from 'react'
import {
  GET_CONSUMPTIONS_FROM_DEVICE,
  GET_DEVICES_FROM_USER,
  GET_OPTIMIZED_CONSUMPTIONS_FROM_DEVICE
} from '../Queries/Queries'
import ConsumptionsGraph from './ConsumptionsGraph'
import { Typography } from '@mui/material'
import DashboardFilters from './DashboardFilters'

const Dashboard = () => {
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
    <>
      {devices.length === 0 &&
        <Typography variant='h4'>No hay dispositivos para mostrar el consumo</Typography>}
      {devices.length > 0 &&
        <DeviceConsumptionInformation devices={devices} />}
    </>
  )
}

const DeviceConsumptionInformation = (props) => {
  const { devices } = props

  const [minDate, setMinDate] = React.useState(new Date('2021-12-05T11:00:00'))
  const [maxDate, setMaxDate] = React.useState(new Date('2021-12-05T23:59:00'))
  const [currentDevice, setCurrentDevice] = React.useState(devices[0].id)
  const [consumptionType, setConsumptionType] = React.useState('real')

  const handleChange = (event) => {
    setCurrentDevice(event.target.value)
  }

  const handleConsumptionChange = (event) => {
    setConsumptionType(event.target.value)
  }

  const handleMinDateChange = (newValue) => {
    setMinDate(newValue)
  }

  const handleMaxDateChange = (newValue) => {
    setMaxDate(newValue)
  }

  const {
    loading: consumptionLoading,
    error: consumptionError,
    data: consumptionData
  } = useQuery(
    GET_CONSUMPTIONS_FROM_DEVICE,
    {
      variables: {
        data: {
          from: format(minDate, 'yyyy-MM-dd HH:mm:ss.000000'),
          to: format(maxDate, 'yyyy-MM-dd HH:mm:ss.000000'),
          device_id: currentDevice
        }
      }
    }
  )

  const {
    loading: optimizedConsumptionLoading,
    error: optimizedConsumptionError,
    data: optimizedConsumptionData
  } = useQuery(
    GET_OPTIMIZED_CONSUMPTIONS_FROM_DEVICE,
    {
      variables: {
        data: {
          from: format(minDate, 'yyyy-MM-dd HH:mm:ss.000000'),
          to: format(maxDate, 'yyyy-MM-dd HH:mm:ss.000000'),
          device_id: currentDevice
        }
      }
    }
  )

  if (consumptionError) {
    console.log(consumptionError)
  }

  if (optimizedConsumptionError) {
    console.log(optimizedConsumptionError)
  }

  let consumptions = []
  let labels = []
  if (consumptionData) {
    consumptions = consumptionData?.getConsumptionsFromDevice?.consumptions?.map(consumption => consumption.consumption_amount)
    labels = consumptionData?.getConsumptionsFromDevice?.consumptions?.map(consumption => consumption.consumption_datetime.substring(5, 22))
  }

  let optimizedConsumptions = []
  let optimizedLabels = []
  if (optimizedConsumptionData) {
    optimizedConsumptions = optimizedConsumptionData?.getOptimizedConsumptionsFromDevice?.optimized_consumptions?.map(consumption => consumption.consumption_amount)
    optimizedLabels = optimizedConsumptionData?.getOptimizedConsumptionsFromDevice?.optimized_consumptions?.map(consumption => consumption.consumption_datetime.substring(5, 22))
  }

  const loadingGraph = (consumptionLoading && consumptionType === 'real') ||
  (optimizedConsumptionLoading && consumptionType === 'optimized')

  const noConsumptions = (consumptionType === 'real' && consumptions.length === 0) ||
  (consumptionType === 'optimized' && optimizedConsumptions.length === 0)

  return (
    <div>
      <DashboardFilters
        devices={devices}
        currentDevice={currentDevice}
        handleChange={handleChange}
        minDate={minDate}
        handleMinDateChange={handleMinDateChange}
        maxDate={maxDate}
        handleMaxDateChange={handleMaxDateChange}
        consumptionType={consumptionType}
        handleConsumptionChange={handleConsumptionChange}
      />
      {loadingGraph &&
        <div>Cargando...</div>}
      {!loadingGraph && noConsumptions &&
        <Typography variant='h5'>No hay consumos de este dispositivo en el rango de fecha seleccionado</Typography>}
      {!loadingGraph && !noConsumptions &&
        <ConsumptionsGraph
          data={consumptionType === 'real' ? consumptions : optimizedConsumptions}
          labels={consumptionType === 'real' ? labels : optimizedLabels}
        />}
    </div>
  )
}

export default Dashboard
