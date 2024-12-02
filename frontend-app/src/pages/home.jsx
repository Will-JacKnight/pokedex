import { useEffect, useState } from 'react';
import titleImg from '../images/pokemon_logo.png';
import PokemonCard from '../components/PokemonCard';
import { Link } from 'react-router-dom';
import SearchBar from '../components/SearchBar';


function Home() {
  const [data, setData] = useState([]);

  useEffect(() => {
    // Fetch data from Flask API using fetch
    if (sessionStorage.getItem('pokemons')) {
      setData(JSON.parse(sessionStorage.getItem('pokemons')));
    }
    else {
      fetch('http://127.0.0.1:5000/api/pokemons')
      .then(response => {
        if (!response.ok) {
          throw new Error('Network response was not ok');
        }
        return response.json();
      })
      .then(rec_data => {
        let arrData = Object.values(rec_data);
        setData(Object.values(arrData)); // convert dictionary to array and store in data state
        sessionStorage.setItem('pokemons', JSON.stringify(arrData));
      })
      .catch(error => console.error('Error fetching data:', error));
    }
    
  }, []);

  const pokemonEl = data?.map((pokemon, index) => {
    return (
      <Link key={index} to={`/details/${pokemon.name}`}>
        <PokemonCard pokemon={pokemon} index={index}>
        </PokemonCard>
      </Link>
    );
  })

    return (
      <>
      <div className="container">
        <SearchBar></SearchBar>
        <img src={titleImg} alt='title' className='title-img'/>
         <div className='pokemon-poster-list'>
              {pokemonEl}
          </div>  
      </div>
      </>
    
    );
  }
  
  export default Home;