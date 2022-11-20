import './InfectionRate.css';


export function InfectionRate(props) {
    console.log("InfectionRate is rendering... " + props.index)

    return (
        <div className={`infection-rate animated`} ></div>
    )
}