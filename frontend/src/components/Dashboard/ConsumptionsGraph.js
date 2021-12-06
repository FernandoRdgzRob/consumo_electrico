import React from 'react'
import Histogram from 'react-chart-histogram'

const ConsumptionsGraph = ({ labels, data }) => {
  // const labels = ['2016', '2017', '2018']
  // const data = [324, 4ss5, 672]
  const options = { fillColor: '#003eff', strokeColor: '#003eff' }

  console.log({ labels, data })
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
