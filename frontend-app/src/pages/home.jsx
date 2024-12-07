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
  const [data, setData] = useState([]); // state to store data
  const [loading, setLoading] = useState(false);  // state to store loading status

  const navigate = useNavigate(); // useNavigate hook to navigate to other pages

  useEffect(() => {
    // Get data from sessionStorage if it exists
    if (sessionStorage.getItem('pokemons')) {
      setData(JSON.parse(sessionStorage.getItem('pokemons')));
    }
    // otherwise fetch from backend
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
        sessionStorage.setItem('pokemons', JSON.stringify(arrData)); // also store in session storage for future use
      })
      .catch(error => console.error('Error fetching data:', error)).finally(() => {
        setLoading(false);
      });
    }
    
  }, []);

  // function to handle logout/login
  function handleAccountClick() {
    // if jwt token is not present, navigate to login page
    if(!sessionStorage.getItem('access_token')) {
      navigate('/login');

    } 
    // if jwt token is present, remove it (thus logging out user) and navigate to home page
    else { 
      alert("You have been logged out successfully!");
      sessionStorage.removeItem('access_token');
      navigate('/');
    }
  }
  
  // Mapping over the data to render PokemonCard components
  const pokemonEl = data?.map((pokemon, index) => {
    return (
        <PokemonCard pokemon={pokemon} index={index} >
        </PokemonCard>
    );
  })
  
    // returning the JSX for the main page
    return (
      <>
      <div className="container">
        <Sidebar /> 
        <SearchBar></SearchBar>
        <img src={titleImg} alt='title' className='title-img'/>
        <img src={accoutImg} alt='title' className='accout-img' onClick={handleAccountClick}/>

   
        <div className='pokemon-poster-list'>
        {/* Conditionally rendering the loading icon if loading is true */}
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