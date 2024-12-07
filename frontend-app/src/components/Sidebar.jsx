import React, { useState } from "react";
import PokemonCard from "./PokemonCard";
import heartImg from "../images/heart.svg";
import closeImg from "../images/closeSymbol.svg"
import { ClipLoader } from 'react-spinners';

const API_BASE_URL = process.env.REACT_APP_API_BASE_URL || 'http://localhost:5000';

// sidebar component
const Sidebar = () => {
  const [isOpen, setIsOpen] = useState(false); // state to store if sidebar is open or not
  const [favourite, setFavourite] = useState([]); // state to store favourite pokemons
  const [loading, setLoading] = useState(false); // state to store loading status

  // function to fetch favourite pokemons from backend
  async function handleFavourite() {
    try {
      // get request to backend to fetch favourite pokemons
      const response = await fetch(`${API_BASE_URL}/favourite`, {
        method: 'GET',
        headers: {
          Authorization: `Bearer ${sessionStorage.getItem('access_token')}`,
        },
      });
      if(!response.ok){
        throw response;
      }
      const data = await response.json();
      setFavourite(Object.values(data)); // convert dictionary to array and store in favourite state
    } catch(reponse) {
      // if response is not successful, remove JWT token and tell user to login again
      if (reponse.status === 401) {
        sessionStorage.removeItem('access_token');
        alert('Token issue. Please login again');
      }
      else {
        alert('Something went wrong. Please try again later');
      }
    } finally {
      setLoading(false);
    }
  }

  // function to toggle sidebar
  const toggleSidebar = () => {
    // if user is logged in, toggle sidebar and fetch favourite pokemons
    if(sessionStorage.getItem('access_token')) {
      setIsOpen(!isOpen);
      handleFavourite();
    }
    // if user is not logged in, tell user to login
    else {
      alert("Please login to see your favourite pokemons");
    }
  };

  // mapping over the favourite pokemons to render PokemonCard components
  const pokemonEl = favourite?.map((pokemon, index) => {
    return (
        <PokemonCard pokemon={pokemon} index={index} sidebar={true}>
        </PokemonCard>
    );
  })

  // returning the JSX for the sidebar
  return (
    <div>
        <img src={heartImg} alt="heart img" onClick={toggleSidebar} className="toggle-button" />
        <div className={`sidebar ${isOpen ? "open" : ""}`}>
            <h2>Your Pokemons</h2>
            <h3 className="add-favourite-msg">To add pokemons to your favourites, double click the pokemon card!</h3>
             {/* conditionally rendering the loader */}
            {loading && <ClipLoader
                  color={"black"}
                  size={50}
                  className='loader'
                />
            }
            {/* if favourite pokemons are not found, show message */}
            {!loading && favourite.length === 0 && <p>You haven't added any pokemons to your favourites</p>}
            <img src={closeImg} alt="close img" onClick={toggleSidebar} className="close-sidebar" />
            <div className='pokemon-poster-list sidebar-list'>
                {pokemonEl}
            </div>
        </div>
        {isOpen && <div className="overlay"></div>}
    </div>
  );
};

export default Sidebar;