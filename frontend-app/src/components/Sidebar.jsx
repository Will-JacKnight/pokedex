import React, { useState } from "react";
import PokemonCard from "./PokemonCard";
import { Link } from "react-router-dom";
import heartImg from "../images/heart.svg";
import closeImg from "../images/closeSymbol.svg"
import { ClipLoader } from 'react-spinners';

const API_BASE_URL = process.env.REACT_APP_API_BASE_URL || 'http://localhost:5000';


const Sidebar = () => {
  const [isOpen, setIsOpen] = useState(false);
  const [favourite, setFavourite] = useState([]);
  const [loading, setLoading] = useState(false);

  async function handleFavourite() {
    try {
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
      setFavourite(Object.values(data));
    } catch(reponse) {
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

  const toggleSidebar = () => {
    if(sessionStorage.getItem('access_token')) {
      setIsOpen(!isOpen);
      handleFavourite();
    }
    else {
      alert("Please login to see your favourite pokemons");
    }
  };

  const pokemonEl = favourite?.map((pokemon, index) => {
    return (
        <PokemonCard pokemon={pokemon} index={index} sidebar={true}>
        </PokemonCard>
    );
  })

  return (
    <div>
        <img src={heartImg} alt="heart img" onClick={toggleSidebar} className="toggle-button" />
        <div className={`sidebar ${isOpen ? "open" : ""}`}>
            <h2>Your Pokemons</h2>
            <h3 className="add-favourite-msg">To add pokemons to your favourites, double click the pokemon card!</h3>
            {loading && <ClipLoader
                  color={"black"}
                  size={50}
                  className='loader'
                />
            }
            {!loading && favourite.length === 0 && <p>You haven't added any pokemons to your favourites</p>}
            {/* <span className="close-sidebar" onClick={toggleSidebar}><strong>X</strong></span> */}
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