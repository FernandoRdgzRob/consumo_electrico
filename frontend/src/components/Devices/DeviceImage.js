import React from 'react'
import Heater from '../../img/heater.svg'
import Microwave from '../../img/microwave.svg'

const DeviceImage = ({ name }) => {
  const dict = {
    calefactor: Heater,
    microondas: Microwave
  }

  return (
    <div
      style={{
        display: 'flex',
        marginTop: 10,
        justifyContent: 'center'
      }}
    >
      <img
        width={80}
        height={80}
        src={dict[name.toLowerCase()]}
        alt='device-image'
      />
    </div>
  )
}

export default DeviceImage
