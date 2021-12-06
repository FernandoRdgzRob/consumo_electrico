import React from 'react'
import DateTimePicker from '@mui/lab/DateTimePicker'
import TextField from '@mui/material/TextField'
import { Grid, MenuItem } from '@mui/material'

const DashboardFilters = (props) => {
  const {
    devices,
    currentDevice,
    handleChange,
    minDate,
    handleMinDateChange,
    maxDate,
    handleMaxDateChange,
    consumptionType,
    handleConsumptionChange
  } = props

  return (
    <Grid container spacing={2} sx={{ mb: 3 }}>
      <Grid item xs>
        <TextField
          fullWidth
          select
          label='Dispositivo'
          value={currentDevice}
          onChange={handleChange}
        >
          {devices.map((device) => (
            <MenuItem key={device.id} value={device.id}>
              {device.name}
            </MenuItem>
          ))}
        </TextField>
      </Grid>
      <Grid item xs>
        <DateTimePicker
          label='Desde:'
          value={minDate}
          onChange={handleMinDateChange}
          renderInput={(params) => {
            console.log({ params })
            return <TextField fullWidth {...params} />
          }}
          inputFormat='dd/MM/yyyy HH:mm'
          ampm={false}
        />
      </Grid>
      <Grid item xs>
        <DateTimePicker
          label='Hasta:'
          value={maxDate}
          onChange={handleMaxDateChange}
          renderInput={(params) => <TextField fullWidth {...params} />}
          inputFormat='dd/MM/yyyy HH:mm'
          ampm={false}
        />
      </Grid>
      <Grid item xs>
        <TextField
          fullWidth
          select
          label='Tipo de consumo'
          value={consumptionType}
          onChange={handleConsumptionChange}
        >
          <MenuItem value='real'>
            Reales
          </MenuItem>
          <MenuItem value='optimized'>
            Optimizados
          </MenuItem>
        </TextField>
      </Grid>
    </Grid>
  )
}

export default DashboardFilters
