import './City.css';
import {Component} from "react";
import {Player} from "../player/Player";



export class City extends Component {
    COLOR_MAPPING = {
        "YELLOW": "yellow-disease",
        "BLACK": "black-disease",
        "BLUE": "blue-disease",
        "RED": "red-disease",
    }
    diseasesArray = []
    styles = {
        position: 'absolute',
        left: this.props.city.position.x,
        top: this.props.city.position.y
    };

    constructor(props) {
        super(props);
        console.log('cities are rendering...')

        Object.keys(this.props.city.diseases).forEach((color) => {
            for(let i = 0; i < this.props.city.diseases[color]; i++) {
                this.diseasesArray.push(color)
            }
        })
    }

    render() {
        return (
            <div style={this.styles} className='city' onClick={() => this.sendAction(this.props.city)}>
                <span className='city-name'>{this.props.city.name}</span>
                <ul className='circle-container'>
                    {
                        this.diseasesArray.map((color, index) =>
                            <li className={`disease ${this.COLOR_MAPPING[color]}`}
                                style={{'--angle': `${360/this.diseasesArray.length*index}deg`}}
                                key={index}
                            ></li>
                        )
                    }
                </ul>
                <ul className='players-container'>
                    {this.props.players.map(player => <li className='player-container'><Player key={player.id} player={player}></Player></li>)}
                </ul>
            </div>
        )
    }

    sendAction(city) {
        console.log(city)
        return null
    }


}



