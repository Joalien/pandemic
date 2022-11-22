import './InfectionRate.css';


export default function InfectionRate(props) {
    console.log("InfectionRate is rendering... " + props.index)

    return (
        <div style={{'--index': props.current_spreading_rate}} className={`infection-rate`} ></div>
    )
}