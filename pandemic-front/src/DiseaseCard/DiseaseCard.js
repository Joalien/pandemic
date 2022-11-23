import {useState} from "react";
import './DiseaseCard.css';


export default function DiseaseCard(props)  {
    const [isFlipped, flipped] = useState(props.card.is_discarded);
    const YELLOW = ['Bogota', 'Buenos Aires', 'Johannesburg', 'Khartoum', 'Kinshasa', 'Lagos', 'Lima', 'Los Angeles', 'Mexico', 'Miami', 'Santiago', 'Sãu Paulo']
    console.log('Disease cards are rendering...')
    console.log(YELLOW.indexOf(props.card.name))
    debugger

    return (
        <div className='scene' onClick={() => flipped(!isFlipped)}>
            <div className={`card ${isFlipped ? 'flip' : ''}`}>
                <div style={{'--index': `${YELLOW.indexOf(props.card.name)}`}} className='front side'></div>
                <div className='back side'></div>
            </div>
        </div>
    )

}



