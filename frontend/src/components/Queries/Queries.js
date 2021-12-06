import { gql } from '@apollo/client'

export const GET_DEVICES_FROM_USER = gql`
  query getDevicesFromUser {
    getDevicesFromUser {
      devices {
        name
        id
        creation_date
        type
      }
      errors
    }
  }
`

export const GET_CONSUMPTIONS_FROM_DEVICE = gql`
  query GetConsumptionsFromDevice($data: GetConsumptionsFromDeviceInput!) {
    getConsumptionsFromDevice(data: $data) {
      consumptions {
        consumption_amount
        consumption_datetime
      }
      errors
    }
  }
`

export const GET_OPTIMIZED_CONSUMPTIONS_FROM_DEVICE = gql`
  query GetOptimizedConsumptionsFromDevice($data: GetOptimizedConsumptionsFromDeviceInput!) {
    getOptimizedConsumptionsFromDevice(data: $data) {
      optimized_consumptions {
        consumption_amount
        consumption_datetime
      }
      errors
    }
  }
`
