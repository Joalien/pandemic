import './City.css';
import {Component} from "react";



export class City extends Component {
    colorMapping = {
        "Color.YELLOW": "yellow-disease",
        "Color.BLACK": "black-disease",
        "Color.BLUE": "blue-disease",
        "Color.RED": "red-disease",
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
                            <li className={`disease ${this.colorMapping[color]}`}
                                style={{'--angle': `${360/this.diseasesArray.length*index}deg`}}
                                key={index}
                            ></li>
                        )
                    }
                </ul>
            </div>
        )
    }

    sendAction(city) {
        console.log(city)
        return null
    }


}



