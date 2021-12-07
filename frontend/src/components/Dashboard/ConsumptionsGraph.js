import React from 'react'
import Histogram from 'react-chart-histogram'

const ConsumptionsGraph = ({ labels, data }) => {
  const options = { fillColor: '#003eff', strokeColor: '#003eff' }

  return (
    <div style={{ display: 'flex', justifyContent: 'center' }}>
      <Histogram
        xLabels={labels}
        yValues={data}
        width='1080'
        height='400'
        options={options}
      />
    </div>
  )
}

export default ConsumptionsGraph
