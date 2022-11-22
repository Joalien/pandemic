import {useState} from "react";
import './DiseaseCard.css';


export default function DiseaseCard()  {
    const [isFlipped, flipped] = useState(false);
    console.log('Disease cards are rendering...')

    return (
        <div className='scene' onClick={() => flipped(!isFlipped)}>
            <div className={`card ${isFlipped ? 'flip' : ''}`}>
                <div className='back'>front</div>
                <div className='back'>back</div>
            </div>
        </div>
    )

}



