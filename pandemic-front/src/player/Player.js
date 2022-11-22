import './Player.css';
import {Component} from "react";



export class Player extends Component {
    PLAYER_SIZE = 13
    CITY_SIZE = 25 // Should not be here

    constructor(props) {
        super(props);
        console.log('players are rendering...')

        this.styles = {
            // left: this.props.player.city.position.x + (this.CITY_SIZE/2 - this.PLAYER_SIZE/2),
            // top: this.props.player.city.position.y,
        }
    }

    render() {
        return (
            <div style={this.styles} className={`player ${this.props.player.is_current_player && 'current-player'}`} onClick={() => this.sendAction(this.props.player)}></div>
        )
    }

    sendAction(city) {
        console.log(city)
        return null
    }


}



