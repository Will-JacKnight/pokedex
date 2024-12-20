import { useEffect, useState } from 'react';
import { useParams, Link } from 'react-router-dom';
import titleImg from '../images/pokemon_logo.png';
import PokemonCard from '../components/PokemonCard';
import eveolutionImg from '../images/evolutions-text.png';
import icons from '../icons';
import homeImg from '../images/home-icon-silhouette.svg';
import sadPikachuImg from '../images/sad-pikachu.gif'
import {ClipLoader} from 'react-spinners';

const API_BASE_URL = process.env.REACT_APP_API_BASE_URL || 'http://localhost:5000';


function Details() {
  const [data, setData] = useState([]); // state to store data
  const [loading, setLoading] = useState(false); // state to store loading status
  const pokemon_name  = useParams().name; // pokemon name from url

  // useEffect to fetch pokemon data from backend
  useEffect(() => {
    window.scrollTo({ top: 0, behavior: "smooth" });
    // Fetch data from Flask API using fetch
    setLoading(true); // set loading to true
    fetch(`${API_BASE_URL}/api/pokemon/${pokemon_name}`)
      .then(response => {
        if (!response.ok) {
          throw new Error('Network response was not ok');
        }
        return response.json();
      })
      .then(rec_data => setData(Object.values(rec_data))) // convert dictionary to array and store in data state
      .catch(error => console.error('Error fetching data:', error)).finally(() => {
        setLoading(false); // set loading to false
      });

  }, [pokemon_name]); // useEffect to fetch data when pokemon_name changes


  // if loading is true, show loader
  if(loading) {
    return (
      <div className="container">
      <Link to='/'><img src={homeImg} className='home-icon' alt="home icon" /></Link>
        <img src={titleImg} alt='title' className='title-img'/>
        <div className='pokemon-profile'>
          <ClipLoader
          color={"black"}
                size={50}
              />
        </div>
      </div>
    );
  }

  // if data is empty, show not found message
  if(data.length === 0) {
    return (
      
      <div className='container'>
        <Link to='/'><img src={homeImg} className='home-icon' alt="home icon" /></Link>
        <img src={titleImg} alt='title' className='title-img'/>
        <div className='pokemon-profile'>
         <h1>Pokemon not found</h1>
         <img src={sadPikachuImg} alt="Crying pikachu gif" className='sad-pikachu' />
        </div>
      </div>
    )
  }

  // find current pokemon in data array
  const currentPokemon = data?.find(pokemon => pokemon.name === pokemon_name);
  // map over the evolutions array to render PokemonCard components exluding current pokemon
  const pokemonEl = data?.map((pokemon, index) => {
    if (pokemon.name !== pokemon_name) {
    return (
        <PokemonCard pokemon={pokemon} index={index} level={true}></PokemonCard>
    );
  } else{
    return null
  }
  })


  // map over the types array to render type icons
  const typeEl = currentPokemon?.types.map((type, index) => {
    return (
        <img key={index}src={icons[type]} alt={type} className='type-icon'/>
    );
  })

  // map over the abilities array to render ability text with specific styling
  const abilitiesEl = currentPokemon?.abilities.map((ability, index) => {
    return (
      <div key={index} className='ability'>
        <p >{ability}</p>
      </div>
    );
  })

  // map over the moves array to render move text wiht specific styling
  const movesEl = currentPokemon?.moves.map((move, index) => {
    return (
      <div key={index} className='move'>
        <p >{move}</p>
      </div>
    );
  })

  // returning the JSX for the details page
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