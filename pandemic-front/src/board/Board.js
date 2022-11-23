import './Board.css';
import board_background from './board.webp'
import {BoardService} from "../services/BoardService"
import InfectionRate from "../Infection-rate/InfectionRate";
import {useEffect, useState} from "react";
import {City} from "../city/City";
import DiseaseCard from "../DiseaseCard/DiseaseCard";


const worldId = 118;

export default function Board() {
    let [board, setBoard] = useState({
        'id': undefined,
        'current_spreading_rate': undefined,
        'number_of_outbreak': undefined,
        'are_antidotes_found': undefined,
        'current_player': undefined,
        'players': undefined,
        'player_cards': undefined,
        'disease_cards': [],
        'cities': undefined
    })
    let [players, setPlayers] = useState([])
    let [cities, setCities] = useState([])
    console.log("Board is rendering")

    useEffect(() => {
        // GET request using fetch inside useEffect React hook
        BoardService.getBoard(worldId)
            .then(board => setBoard(board));
        BoardService.getAllCities(worldId)
            .then(cities => setCities(cities));
        BoardService.getAllPlayers(worldId)
            .then(players => {
                players.forEach(player => BoardService.getIndexOfPlayerInCity(worldId, player).then(index => player['index'] = index)) // callback hell?
                setPlayers(players)
            });

// empty dependency array means this effect will only run once (like componentDidMount in classes)
    }, []);

    return (
        <div style={{backgroundImage: `url(${board_background})`, backgroundRepeat: "no-repeat"}} className='Board'>
            <InfectionRate current_spreading_rate={board.current_spreading_rate}></InfectionRate>
            <ul>
                {board.disease_cards.map(disease_card => <li><DiseaseCard key={disease_card.id} card={disease_card}></DiseaseCard></li>)}
            </ul>
            <ul>
                {cities.map(city => <li><City key={city.id} city={city} players={players.filter(p => p.city.id === city.id)}></City></li>)}
            </ul>
        </div>
    );
}
