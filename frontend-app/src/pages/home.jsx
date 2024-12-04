import { useEffect, useState } from 'react';
import titleImg from '../images/pokemon_logo.png';
import accoutImg from '../images/login-logout.jpg';
import PokemonCard from '../components/PokemonCard';
import { Link, useNavigate, useLocation } from 'react-router-dom';
import SearchBar from '../components/SearchBar';
import Sidebar from '../components/Sidebar';


function Home() {
  const [data, setData] = useState([]);
  const navigate = useNavigate();

  useEffect(() => {
    // Fetch data from Flask API using fetch
    if (sessionStorage.getItem('pokemons')) {
      setData(JSON.parse(sessionStorage.getItem('pokemons')));
    }
    else {
      fetch('https://pokedex.impaas.uk/api/pokemons')
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

  function handleAccountClick() {
    if(!sessionStorage.getItem('access_token')) {
      navigate('/login');
    } else { 
      alert("You have been logged out successfully!");
      sessionStorage.removeItem('access_token');
      navigate('/');
    }
  }
  
  console.log(data);
  const pokemonEl = data?.map((pokemon, index) => {
    return (
      // <Link key={index} to={`/details/${pokemon.name}`}>
        <PokemonCard pokemon={pokemon} index={index} >
        </PokemonCard>
      // </Link>
    );
  })

    return (
      <>
      <div className="container">
        <Sidebar />
        <SearchBar></SearchBar>
        <img src={titleImg} alt='title' className='title-img'/>
        <img src={accoutImg} alt='title' className='accout-img' onClick={handleAccountClick}/>

         <div className='pokemon-poster-list'>
              {pokemonEl}
          </div>  
      </div>
      </>
    
    );
  }
  
  export default Home;