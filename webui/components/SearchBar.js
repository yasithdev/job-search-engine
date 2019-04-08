const SearchBar = (props) => (
    <form action="/search" method="get" className="mb-0 pb-0">
        <div className="form-group">
            <div className="input-group">
                <input type="text" className="form-control" name="query" placeholder="Search" defaultValue={props.text}></input>
                <i className="fa fa-search" style={{position: "absolute", right: "10px", top: "10px", zIndex: "5"}}></i>
            </div>
            <input type="submit" value="Search" hidden></input>
        </div>
    </form>
)

export default SearchBar