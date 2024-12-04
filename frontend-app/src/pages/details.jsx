import { useEffect, useState } from 'react';
import { useParams, Link } from 'react-router-dom';
import titleImg from '../images/pokemon_logo.png';
import PokemonCard from '../components/PokemonCard';
import eveolutionImg from '../images/evolutions-text.png';
import icons from '../icons';
import homeImg from '../images/home-icon-silhouette.svg';

const API_BASE_URL = process.env.REACT_APP_API_BASE_URL || 'http://localhost:5000';


function Details() {
  const [data, setData] = useState([]);
  const pokemon_name  = useParams().name;

  useEffect(() => {
    window.scrollTo({ top: 0, behavior: "smooth" });
    // Fetch data from Flask API using fetch
    fetch(`${API_BASE_URL}/api/pokemon/${pokemon_name}`)
      .then(response => {
        if (!response.ok) {
          throw new Error('Network response was not ok');
        }
        return response.json();
      })
      .then(rec_data => setData(Object.values(rec_data))) // convert dictionary to array and store in data state
      .catch(error => console.error('Error fetching data:', error));
  }, [pokemon_name]);


  const currentPokemon = data?.find(pokemon => pokemon.name === pokemon_name);

  console.log(data);
  const pokemonEl = data?.map((pokemon, index) => {
    if (pokemon.name !== pokemon_name) {
    return (
        <PokemonCard pokemon={pokemon} index={index} level={true}></PokemonCard>
    );
  } else{
    return null
  }
  })


  const typeEl = currentPokemon?.types.map((type, index) => {
    return (
        <img key={index}src={icons[type]} alt={type} className='type-icon'/>
    );
  })

  const abilitiesEl = currentPokemon?.abilities.map((ability, index) => {
    return (
      <div key={index} className='ability'>
        <p >{ability}</p>
      </div>
    );
  })

  const movesEl = currentPokemon?.moves.map((move, index) => {
    return (
      <div key={index} className='move'>
        <p >{move}</p>
      </div>
    );
  })

  return (
    <>
      <div className="container">
        <Link to='/'><img src={homeImg} className='home-icon' alt="home icon" /></Link>
        <img src={titleImg} alt='title' className='title-img'/>
        <div className='pokemon-profile'>
          <h2>{currentPokemon?.name[0].toUpperCase() + currentPokemon?.name.slice(1)}</h2>
          <h3 className='hp hp-profile'>HP: {currentPokemon?.hp}</h3>
          <div className='types-container'>{typeEl}</div>
          <img src={currentPokemon?.image} alt='title' className='pokemon-img'/>
          <p className='pokemon-description'>{currentPokemon?.description.replace(/\f/g, ' ')}</p>
          <div>
            <div className='pokemon-stats'>
              <p><strong>ATT</strong>&nbsp;&nbsp;{currentPokemon?.attack}</p> 
              <p><strong>DEF</strong>&nbsp;&nbsp;{currentPokemon?.defense}</p>
            </div>
            <div className='pokemon-stats'>
              <p><strong>WEIGHT</strong>&nbsp;&nbsp;{currentPokemon?.weight}</p>
              <p><strong>SPEED</strong>&nbsp;&nbsp;{currentPokemon?.speed}</p>
            </div>
            <div className="pokemon-stats">
              <p><strong>EVOLUTION LV.</strong>&nbsp;&nbsp;{currentPokemon?.level}</p>
            </div>
          </div>
          <h5 className='abilities-title'>Abilities</h5>
          <div className='abilities-container'>
            {abilitiesEl}
          </div>
          <h5 className='moves-title'>Moves</h5>
          <div className='moves-container'>
            {movesEl}
          </div>
        </div>
        <img src={eveolutionImg} alt='title' className='title-img'/>
        <div className='pokemon-poster-list'>
          {pokemonEl}
        </div>
      </div>
      
    </>
  )

  }
  
  export default Details;