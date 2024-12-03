import React, { useState } from "react";
import PokemonCard from "./PokemonCard";
import { Link } from "react-router-dom";
import heartImg from "../images/heart.svg";

const Sidebar = () => {
  const [isOpen, setIsOpen] = useState(false);
  const [favourite, setFavourite] = useState([]);

  async function handleFavourite() {
    try {
      const response = await fetch('http://127.0.0.1:5000/favourite', {
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

//   console.log(favourite);

  const pokemonEl = favourite?.map((pokemon, index) => {
    return (
      // <Link key={index} to={`/details/${pokemon.name}`}>
        <PokemonCard pokemon={pokemon} index={index} sidebar={true}>
        </PokemonCard>
      // </Link>
    );
  })

  return (
    <div>
        <img src={heartImg} alt="heart img" onClick={toggleSidebar} className="toggle-button" />

        <div className={`sidebar ${isOpen ? "open" : ""}`}>
            <h2>Your Pokemons</h2>
            {favourite.length === 0 && <p>You haven't added any pokemons to your favourites</p>}
            <span className="close-sidebar" onClick={toggleSidebar}><strong>X</strong></span>
            <div className='pokemon-poster-list sidebar-list'>
                {pokemonEl}
            </div>
        </div>
        {isOpen && <div className="overlay"></div>}
    </div>
  );
};

export default Sidebar;