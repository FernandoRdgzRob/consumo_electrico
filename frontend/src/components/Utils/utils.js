import React from 'react'
// Material UI
import { Button, Grid, MenuItem, TextField } from '@mui/material'
// React Hook Form
import { useController } from 'react-hook-form'

// Form helpers
export function useCustomController (props) {
  const { name, control, rules, defaultValue, ...rest } = props
  const controllerFunctions = useController({ name, control, rules, defaultValue })
  return { ...controllerFunctions, ...rest }
}

export const CustomInput = ({ form, handleSubmit, onSubmit, button, onCancel }) => {
  const formArray = Object.keys(form)

  return (
    <form onSubmit={handleSubmit(onSubmit)}>
      <Grid
        container
        direction='row'
        justifyContent='center'
        alignItems='center'
        spacing={3}
      >
        {formArray.map((field, index) => {
          console.log(form[field])
          const {
            field: { ref, value, ...inputProps },
            fieldState: { error },
            formState,
            type,
            options,
            ...otherProps
          } = form[field]

          return (
            <Grid key={index} item xs={12} sx={{ mb: 2 }}>
              <TextField
                error={!!error}
                fullWidth
                helperText={error?.message || ''}
                inputRef={ref}
                type={type || 'text'}
                select={type === 'select'}
                value={value || ''}
                {...inputProps}
                {...otherProps}
              >
                {type === 'select' &&
                  options.map((option) => (
                    <MenuItem key={option.value} value={option.value}>
                      {option.label}
                    </MenuItem>
                  ))}
              </TextField>
            </Grid>
          )
        })}
        {
          onCancel &&
            <Grid item xs={6}>
              <Button onClick={onCancel} variant='outlined' fullWidth>
                Cancelar
              </Button>
            </Grid>
        }
        <Grid item xs={onCancel ? 6 : 12}>
          <Button type='submit' variant='contained' fullWidth>
            {button || 'Enviar'}
          </Button>
        </Grid>
      </Grid>
    </form>
  )
}
