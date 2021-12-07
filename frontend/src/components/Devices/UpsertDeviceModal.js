import * as React from 'react'
import Dialog from '@mui/material/Dialog'
import DialogContent from '@mui/material/DialogContent'
import { CustomInput, useCustomController } from '../Utils/utils'
import { useForm } from 'react-hook-form'
import { Typography } from '@mui/material'
import { devicesInformation } from './devicesInformation'
import { UPSERT_DEVICE } from '../Mutations/Mutations'
import { useMutation } from '@apollo/client'
import { GET_DEVICES_FROM_USER } from '../Queries/Queries'
import { useSnackbar } from 'notistack'

const UpsertDeviceModal = ({ open, setOpen }) => {
  const { control, handleSubmit, reset } = useForm({ shouldUnregister: true })
  const { enqueueSnackbar } = useSnackbar()

  const handleClose = () => {
    setOpen(false)
  }

  const handleOnCompleted = (data) => {
    reset()
    setOpen(false)
    enqueueSnackbar('Dispositivo agregado manera exitosa', { variant: 'success' })
  }

  const handleError = (error) => {
    console.log(error)
  }

  const [upsertDevice] = useMutation(UPSERT_DEVICE, {
    onCompleted: handleOnCompleted,
    onError: handleError,
    refetchQueries: [
      { query: GET_DEVICES_FROM_USER }
    ],
    awaitRefetchQueries: true
  })

  const onSubmit = (data) => {
    const deviceMetrics = devicesInformation[data.type.toLowerCase()]
    const input = {
      ...deviceMetrics,
      ...data
    }
    upsertDevice({ variables: { data: input } })
  }

  const form = {
    name: useCustomController({
      name: 'name',
      control,
      rules: { required: 'El nombre del dispositivo es requerido' },
      label: 'Nombre del dispositivo',
      type: 'text',
      placeholder: 'Ventilador de la sala',
      defaultValue: ''
    }),
    type: useCustomController({
      name: 'type',
      control,
      rules: { required: 'El dispositivo es requerido' },
      label: 'Dispositivo',
      type: 'select',
      options: [
        { value: 'Calefactor', label: 'Calefactor' },
        { value: 'Aire', label: 'Aire' },
        { value: 'Ventilador', label: 'Ventilador' },
        { value: 'Secadora', label: 'Secadora' },
        { value: 'Lavatrastes', label: 'Lavatrastes' },
        { value: 'Estufa', label: 'Estufa' },
        { value: 'Microondas', label: 'Microondas' },
        { value: 'Lavadora', label: 'Lavadora' },
        { value: 'Refrigerador', label: 'Refrigerador' },
        { value: 'Foco', label: 'Foco' }
      ],
      defaultValue: null
    })
  }

  return (
    <div>
      <Dialog open={open} onClose={handleClose}>
        <DialogContent style={{ width: 500 }}>
          <Typography sx={{ mb: 5 }} variant='h5'>Agregar dispositivo</Typography>
          <CustomInput
            form={form}
            handleSubmit={handleSubmit}
            onSubmit={onSubmit}
            button='Agregar'
            onCancel={handleClose}
          />
        </DialogContent>
      </Dialog>
    </div>
  )
}

export default UpsertDeviceModal
