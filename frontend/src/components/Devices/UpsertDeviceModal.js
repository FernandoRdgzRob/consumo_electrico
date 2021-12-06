import * as React from 'react'
import Dialog from '@mui/material/Dialog'
import DialogContent from '@mui/material/DialogContent'
import { CustomInput, useCustomController } from '../Utils/utils'
import { useForm } from 'react-hook-form'
import { Typography } from '@mui/material'

const UpsertDeviceModal = ({ open, setOpen }) => {
  const { control, handleSubmit } = useForm()

  const handleClose = () => {
    setOpen(false)
  }

  const onSubmit = (data) => {
    console.log({ data })
  }

  const form = {
    type: useCustomController({
      name: 'type',
      control,
      rules: { required: 'El dispositivo es requerido' },
      label: 'Dispositivo',
      type: 'select',
      options: [
        { value: 'UI', label: 'Calefactor' },
        { value: 'UX', label: 'Aire' },
        { value: 'Enhancement', label: 'Ventilador' },
        { value: 'Bug', label: 'Secadora' },
        { value: 'Feature', label: 'Lavatrastes' },
        { value: 'Feature', label: 'Estufa' },
        { value: 'Feature', label: 'Microondas' },
        { value: 'Feature', label: 'Lavadora' },
        { value: 'Feature', label: 'Refrigerador' },
        { value: 'Feature', label: 'Foco' }
      ]
    })
    // name: useCustomController({
    //   name: 'name',
    //   control,
    //   rules: { required: 'El nombre del dispositivo es requerido' },
    //   label: 'Nombre del dispositivo',
    //   type: 'text',
    //   placeholder: 'Ventilador de la sala'
    // })
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
