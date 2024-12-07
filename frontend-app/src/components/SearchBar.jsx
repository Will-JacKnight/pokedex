import { useNavigate } from "react-router-dom"
import { useState } from "react"
import searchImg from "../images/search-icon.svg"

// Searchbar component
export default function SearchBar() {

    const [searchQuery, setSearchQuery] = useState("") // the user search string
    const navigate = useNavigate() 

    // whenever the user change the input, the searchQuery state is updated
    function handleChange(e) {
        setSearchQuery(e.target.value)
    }

    // When submission happens, the final version of the searchQuery is saved in sessionStorage and the user is redirected to the results page
    function handleSubmit(e) {
        e.preventDefault()
        setSearchQuery("")
        navigate(`/details/${searchQuery.toLowerCase()}`)
    }
    // JSX for searchbar
    return (
        <div className="search-box">
            <div className="relative">
                <img src={searchImg} alt="search-icon" className="serach-icon"/>
                <form onSubmit={handleSubmit}>
                    <input 
                        type="text" 
                        placeholder="Search here" 
                        value={searchQuery}
                        onChange={handleChange}
                    />
                </form>
            </div>
        </div>
    )
}