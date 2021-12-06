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
