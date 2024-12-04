import {levels} from '../icons';
import heartImg from '../images/heart.svg';
import { Link, useNavigate } from 'react-router-dom';
import { useState, useRef } from 'react';

const API_BASE_URL = process.env.REACT_APP_API_BASE_URL || 'http://localhost:5000';


function PokemonCard({pokemon, index, level=false, sidebar=false}) {
  const doubleClickRef = useRef(false);
  const navigate = useNavigate();

  async function addFavourite(pokemon_name) {
    try {
      const response = await fetch(`${API_BASE_URL}/addFavourite`, {
        method: 'POST',
        headers: {
            Authorization: `Bearer ${sessionStorage.getItem('access_token')}`,
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            "pokemon_name": pokemon_name,
        }),
      });
      if(!response.ok){
        throw response;
      }
      const data = await response.json();
      if(data.success) {
        alert("You have added this pokemon to your favourites successfully!");
      }
    }
    catch(reponse) {
      if (reponse.status === 401) {
        sessionStorage.removeItem('access_token');
        alert('Token issue. Please login again');
      }
      else {
        alert('Something went wrong. Please try again later');
      }
    }
  }

  async function removeFavourite() {
    try {
      const response = await fetch(`${API_BASE_URL}/removeFavourite`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${sessionStorage.getItem('access_token')}`
        },
        body: JSON.stringify({
            "pokemon_name": pokemon.name,
        }),
     });
      if(!response.ok){
        throw response;
      }
      const data = await response.json();
      if(data.success) {
          navigate('/',  { state: { refresh: Date.now() } });
          window.location.reload();
          alert("You have removed this pokemon from your favourites successfully!");
      }
    }
    catch(reponse) {
      if (reponse.status === 401) {
        sessionStorage.removeItem('access_token');
        alert('Token issue. Please login again');
      }
      else {
        alert('Something went wrong. Please try again later');
        }
      }
  }

  let clickTimeout = null;

  const handleClick = () => {
    if (clickTimeout) {
      clearTimeout(clickTimeout); // Cancel the single-click timer
    }
    clickTimeout = setTimeout(() => {
      if (!doubleClickRef.current) {
        navigate(`/details/${pokemon.name}`); // Only navigate if no double-click occurred
      }
    }, 600); // Adjust delay to fit double-click recognition timing
  };
  
  const handleDoubleClick = () => {
    if (!sidebar) {
      if (clickTimeout) {
        clearTimeout(clickTimeout); // Cancel the single-click timer
        clickTimeout = null;
      }
      doubleClickRef.current = true; // Mark that a double-click occurred
      if(sessionStorage.getItem('access_token')) {
        addFavourite(pokemon.name);
      }
      else {
        alert("Please login to add pokemons to your favourites");
      }
      setTimeout(() => {
        doubleClickRef.current = false; // Reset double-click flag
      }, 600); 
    }
  };

  // console.log(pokemon)
  // if (pokemon.length === 0) {
  //   console.log("Pokemon is null");
  //   return null
  // }

  return (

      <div className='card-container' key={index}>
        <div  className='pokemon-poster normal-type' onClick={handleClick} onDoubleClick={handleDoubleClick}>
          {level && <img className='pokemon-level' src={levels[`lv${pokemon.level}`]} alt='level' />}
          <h3 className='hp'>HP: {pokemon.hp}</h3>
          <div> 
            <h3 className='pokemon-name'>{pokemon?.name[0].toUpperCase() + pokemon?.name.slice(1)}</h3>
          </div>
          <img src={pokemon.image} alt={pokemon.name} className='pokemon-poster-img'/>
          {/* <img src={heartImg} alt={pokemon.name} className='pokemon-poster-img card-heart'onClick={handleHeartClick}/> */}

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
        {sidebar && <p className='remove-pokemon' onClick={removeFavourite}>Remove Pokemon</p>   }   
      </div>

      
  );
}

export default PokemonCard;