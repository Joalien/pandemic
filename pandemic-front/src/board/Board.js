import './Board.css';
import board from './board.webp'
import {City} from "../city/City";
import {CityService} from "../services/CityService"
import {InfectionRate} from "../Infection-rate/InfectionRate";


export default function Board() {
    let cities = CityService.getAllCities();
    console.log("Board is rendering")

    return (<div style={{backgroundImage: `url(${board})`, backgroundRepeat: "no-repeat"}} className='Board'>
        <InfectionRate index={0}></InfectionRate>
        <ul>
            {cities.map(city => <li><City key={city.name} city={city}></City></li>)}
        </ul>
    </div>);
}
