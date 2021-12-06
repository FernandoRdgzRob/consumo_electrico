import React from 'react'
import Heater from '../../img/heater.svg'
import Microwave from '../../img/microwave.svg'
import Stove from '../../img/stove.svg'
import Air from '../../img/air.svg'
import Bulb from '../../img/bulb.svg'
import Dishwasher from '../../img/dishwasher.svg'
import DryingMachine from '../../img/drying-machine.svg'
import Fan from '../../img/fan.svg'
import Fridge from '../../img/fridge.svg'
import WashingMachine from '../../img/washing-machine.svg'

const DeviceImage = ({ name }) => {
  const dict = {
    calefactor: Heater,
    microondas: Microwave,
    estufa: Stove,
    aire: Air,
    foco: Bulb,
    lavatrastes: Dishwasher,
    secadora: DryingMachine,
    ventilador: Fan,
    refrigerador: Fridge,
    lavadora: WashingMachine
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
        alt='device'
      />
    </div>
  )
}

export default DeviceImage
