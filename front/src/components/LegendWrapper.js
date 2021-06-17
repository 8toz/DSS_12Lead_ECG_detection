import React, {useState} from 'react';
import Legend from "./Legend"
import DecBar from "./DecBar"

function LegendWrapper(props) {
    const [open,setOpen] = useState(false)
    return (
        <>
        <DecBar setDarkTheme={props.setDarkTheme} 
                setOpen={setOpen} 
                open={open} 
                darkTheme={props.darkTheme}/>

        <Legend open={open}
                setOpen={setOpen}/>
        </>
    );
}

export default LegendWrapper;