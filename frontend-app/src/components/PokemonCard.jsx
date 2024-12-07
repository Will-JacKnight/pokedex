import {levels} from '../icons';
import { useNavigate } from 'react-router-dom';
import { useRef } from 'react';

const API_BASE_URL = process.env.REACT_APP_API_BASE_URL || 'http://localhost:5000';

// pokemon card component

function PokemonCard({pokemon, index, level=false, sidebar=false}) {
  const doubleClickRef = useRef(false); // used to track double click
  const navigate = useNavigate(); // used to navigate to other pages

  // function to add pokemon to favourites list of user
  async function addFavourite(pokemon_name) {
    // psot request to backend to add pokemon to favourites list of user
    try {
      const response = await fetch(`${API_BASE_URL}/addFavourite`, {
        method: 'POST',
        // include JWT token in header for authentication
        headers: {
            Authorization: `Bearer ${sessionStorage.getItem('access_token')}`,
            'Content-Type': 'application/json',
        },
        // send pokemon_name to be added to favourites list
        body: JSON.stringify({
            "pokemon_name": pokemon_name,
        }),
      });
      if(!response.ok){
        throw response;
      }
      const data = await response.json();
      // if response is successful, tell user that pokemon was added to favourites list
      if(data.success) {
        alert("You have added this pokemon to your favourites successfully!");
      }
    }
    catch(reponse) {
      // if response is not successful, remove JWT token and tell user to login again
      if (reponse.status === 401) {
        sessionStorage.removeItem('access_token');
        alert('Token issue. Please login again');
      }
      else {
        alert('Something went wrong. Please try again later');
      }
    }
  }

  // function to remove pokemon from favourites list of user
  async function removeFavourite() {
    try {
      // post request to backend to remove pokemon from favourites list of user
      const response = await fetch(`${API_BASE_URL}/removeFavourite`, {
        method: 'POST',
        // include JWT token in header for authentication
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${sessionStorage.getItem('access_token')}`
        },
        // send pokemon_name to be removed from favourites list
        body: JSON.stringify({
            "pokemon_name": pokemon.name,
        }),
     });
      if(!response.ok){
        throw response;
      }
      const data = await response.json();
      // if response is successful, navigate to home page and refresh page
      if(data.success) {
          navigate('/',  { state: { refresh: Date.now() } });
          window.location.reload();
          // tell user that pokemon was removed from favourites list
          alert("You have removed this pokemon from your favourites successfully!");
      }
    }
    catch(reponse) {
      // if response is not successful, remove JWT token and tell user to login again
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

  // function to handle click on pokemon card
  // on single click, navigate to details page
  const handleClick = () => {
    if (clickTimeout) {
      clearTimeout(clickTimeout); // Cancel the single-click timer
    }
    clickTimeout = setTimeout(() => {
      if (!doubleClickRef.current) {
        navigate(`/details/${pokemon.name}`);
      }
    }, 600); // after delay, if no double click, navigate to details page
  };
  
  // function to handle double click on pokemon card
  // on double click, add pokemon to favourites list of user
  // if not logged in, tell user to login
  const handleDoubleClick = () => {
    if (!sidebar) {
      if (clickTimeout) {
        clearTimeout(clickTimeout); // Cancel the single-click timer
        clickTimeout = null;
      }
      doubleClickRef.current = true; // Mark that a double-click occurred
      // if user is logged in, add pokemon to favourites list of user
      if(sessionStorage.getItem('access_token')) {
        addFavourite(pokemon.name);
      }
      // if user is not logged in, tell user to login
      else {
        alert("Please login to add pokemons to your favourites");
      }
      setTimeout(() => {
        doubleClickRef.current = false; // Reset double-click flag
      }, 600); 
    }
  };

  // return the JSX for the pokemon card
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