import Link from 'next/link'

const titleStyle = {
    marginRight: 15
}

const bodyStyle = {
    marginLeft: 15
}

const SearchResult = props => (
    <Link href={props.item.url}>
        <div>
            <a style={titleStyle}>{props.item.title}</a>
            <p>Site: {props.item.site}</p>
            <p>Posted On: {props.item.datePosted}</p>
            <p>Hired By: {props.item.hiredBy}</p>
            <a style={bodyStyle}>{props.item.description}</a>
        </div>
    </Link>
)

export default SearchResult