import { Container, Grid, MenuItem, TextField } from '@mui/material';
import { useEffect, useState } from 'react';
import { AdapterMoment } from '@mui/x-date-pickers/AdapterMoment';
import { LocalizationProvider } from '@mui/x-date-pickers/LocalizationProvider';
import { DesktopDatePicker } from '@mui/x-date-pickers/DesktopDatePicker';
import { LineChart, Line, CartesianGrid, XAxis, YAxis, Tooltip, ReferenceLine, ReferenceArea, ResponsiveContainer, Legend } from 'recharts';
import testProfiles from '../profiles';


function getRandomColor(i) {
    const colors = ['#8884d8', '#82ca9d', 'purple', 'green', 'teal', 'blue', 'orange', 'brown', 'gray', ''];
    return colors[i % colors.length];
  }


const ChartArea = (props) => {
    const userId = props.userId;

    const [chart, updateChart] = useState({profile: testProfiles[0],
                                           end: new Date(),
                                           start: new Date(new Date().setFullYear(new Date().getFullYear()-5))});
    const [chartKeys, updateChartKeys] = useState([]);
    const [chartData, updateChartData] = useState({profile: '', data: [], tests: [], units: {}, reference: {}, range: {}});

    const renderChart = () => {
        fetch("http://localhost:8000/report-reader/v1/report/",
        { method: 'POST',
          headers: {'Content-Type': 'application/json'},
          credentials: 'include',
          body: JSON.stringify({
                    user_id: userId,
                    start_date: chart.start,
                    end_date: chart.end,
                    profile: chart.profile,
                })
        })
        .then(response=>{
            if(!response.ok) throw new Error(response.status);
            else return response.json();
        })
        .then((results)=>{
            updateChartData(results);
            updateChartKeys(results.tests);
        });
    };

    useEffect(()=>{renderChart()}, [chart]);

    const handleTestChange = (e) => {
        var test = e.target.value;
        if(test==='ALL'){
            updateChartKeys(chartData.tests);
        } else {
            updateChartKeys([test]);
        }
    };

    return (
        <Container>
        <Grid container direction="column" justifyContent="right">
            <Grid item container justifyContent="right" alignItems="flex-end">
                <Grid item style={{margin: 8}}>
                    <TextField
                        select
                        size='small'
                        value={chartKeys.length == 1 ? chartKeys[0]: 'ALL'}
                        label="Test"
                        onChange={handleTestChange}
                        >
                        <MenuItem key='ALL' value='ALL'>ALL</MenuItem>
                        {chartData.tests.map(item=><MenuItem key={item} value={item}>{item}</MenuItem>)}
                    </TextField>
                </Grid>
                <Grid item style={{margin: 8}}>
                    <TextField
                        select
                        size='small'
                        value={chart.profile}
                        label="Profile"
                        onChange={(e)=>updateChart((state)=>({...state, profile: e.target.value}))}
                        >
                        {testProfiles.map(item=><MenuItem key={item} value={item}>{item}</MenuItem>)}
                    </TextField>
                </Grid>
            </Grid>
            <Grid item container justifyContent="right" alignItems="flex-end">
                <Grid item style={{margin: 8}} >
                    <LocalizationProvider dateAdapter={AdapterMoment}>
                        <DesktopDatePicker

                            label="Start Date"
                            inputFormat="MM/DD/YYYY"
                            value={chart.start}
                            minDate="01/01/2000"
                            maxDate={new Date().toDateString()}
                            onChange={(val)=>updateChart((state)=>({...state, start: new Date(val)}))}
                            renderInput={(params) => <TextField {...params} />}
                        />

                    </LocalizationProvider>

                </Grid>
                <Grid item style={{margin: 8}}>
                    <LocalizationProvider dateAdapter={AdapterMoment}>
                        <DesktopDatePicker
                            label="End Date"
                            inputFormat="MM/DD/YYYY"
                            value={chart.end}
                            minDate="01/01/2000"
                            maxDate={new Date().toDateString()}
                            onChange={(val)=>updateChart((state)=>({...state, end: new Date(val)}))}
                            renderInput={(params) => <TextField {...params} />}
                        />
                    </LocalizationProvider>
                </Grid>

            </Grid>
            
            <Grid item style={{height: '400px', width: 'inherit', paddingRight: 8}}>
                    <ResponsiveContainer height="100%" width='100%'>
                    <LineChart  data={chartData.data} margin={{ top: 20, right: 0, bottom: 5, left: 0 }}>
                        {chartKeys.length === 1? <ReferenceLine alwaysShow y={chartData.range[chartKeys[0]][1]} label="Normal Max" stroke="red" />: null}
                        {chartKeys.length === 1? <ReferenceLine alwaysShow y={chartData.range[chartKeys[0]][0]} label="Normal Min" stroke="red" />: null}
                        {chartKeys.length === 1? chartData.reference[chartKeys[0]].map(ref=>
                        <ReferenceArea alwaysShow y1={ref[1][0]} y2={ref[1][1]} label={ref[0]} strokeOpacity={0.9} stroke="pink" />): null}
                        {chartKeys.map((item, i)=><Line connectNulls key={i} type="monotone" dataKey={item} stroke={getRandomColor(i)} />)}
                        <CartesianGrid stroke="#ccc" strokeDasharray="3 3" />
                        <XAxis dataKey="key" />
                        <Tooltip />
                        <YAxis label={{value: chartKeys.length === 1? chartData.units[chartKeys[0]]: null, angle: -90, position: 'insideLeft'}}/>
                        {chartKeys.length<=10?<Legend />:null}
                    </LineChart>
                    </ResponsiveContainer>
            </Grid>
        </Grid>
    </Container>
    );
};
 
export default ChartArea;