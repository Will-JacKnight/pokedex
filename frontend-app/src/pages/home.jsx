import { useEffect, useState } from 'react';
import titleImg from '../images/pokemon_logo.png';
import accoutImg from '../images/login-logout.jpg';
import PokemonCard from '../components/PokemonCard';
import { useNavigate } from 'react-router-dom';
import SearchBar from '../components/SearchBar';
import Sidebar from '../components/Sidebar';
import { ClipLoader } from 'react-spinners';

const API_BASE_URL = process.env.REACT_APP_API_BASE_URL || 'http://localhost:5000';

function Home() {
  const [data, setData] = useState([]);
  const [loading, setLoading] = useState(false);

  const navigate = useNavigate();

  useEffect(() => {
    // Fetch data from Flask API using fetch
    if (sessionStorage.getItem('pokemons')) {
      setData(JSON.parse(sessionStorage.getItem('pokemons')));
    }
    else {
      setLoading(true);
      fetch(`${API_BASE_URL}/api/pokemons`)
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
      .catch(error => console.error('Error fetching data:', error)).finally(() => {
        setLoading(false);
      });
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
            {loading && <ClipLoader
                  color={"white"}
                  size={100}
                  className='loader'
                />
            }
            {!loading && pokemonEl}
        </div> 
        
      </div>
      </>
    
    );
  }
  
  export default Home;