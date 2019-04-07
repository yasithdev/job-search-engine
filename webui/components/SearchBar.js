const SearchBar = (props) => (
    <form action="/search" method="get">
        <input type="text" name="query" placeholder="Enter search keyword(s)" defaultValue={props.text}></input>
        <input type="submit" value="Search"></input>
    </form>
)

export default SearchBar