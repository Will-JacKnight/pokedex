import {levels} from '../icons';


function PokemonCard({pokemon, index, level=false}) {

    return (
    <div key={index} className='pokemon-poster normal-type' >
      {level && <img className='pokemon-level' src={levels[`lv${pokemon.level}`]} alt='level' />}
      <h3 className='hp'>HP: {pokemon.hp}</h3>
      <div> 
        <h3 className='pokemon-name'>{pokemon.name[0].toUpperCase() + pokemon.name.slice(1)}</h3>
      </div>
      <img src={pokemon.image} alt={pokemon.name} className='pokemon-poster-img'/>
      <div className='stats-container'>
        <div className='pokemon-stats'>
          <p><strong>ATT</strong>&nbsp;&nbsp;{pokemon.attack}</p> 
          <p><strong>DEF</strong>&nbsp;&nbsp;{pokemon.defense}</p>
        </div>
        <div className='pokemon-stats'>
          <p><strong>WEIGHT</strong>&nbsp;&nbsp;{pokemon.weight}</p>
          <p><strong>SPEED</strong>&nbsp;&nbsp;{pokemon.speed}</p>
        </div>
      </div>        
    </div>
        
      );
}

export default PokemonCard;