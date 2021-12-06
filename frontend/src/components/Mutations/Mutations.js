import { gql } from '@apollo/client'

export const LOGIN = gql`
  mutation Login($data: loginInput!) {
    login(data: $data) {
      success
      errors
      user {
        name
      }
      token {
        value
      }
    }
  }
`

export const UPSERT_DEVICE = gql`
  mutation UpsertDevice($data: UpsertDeviceInput!) {
    upsertDevice(data: $data) {
      device {
        name
      }
      errors
      success
    }
  }
`
