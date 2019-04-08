import Link from 'next/link'
import moment from 'moment'

function truncate(str, num) {
    if (str.length > num) {
        return str.slice(0, num) + "...";
    }
    else {
        return str;
    }
}

function postedInfo(date, employee, score) {
    if (date || employee) {
        return <span>Posted{date? <b> {moment(date).fromNow()}</b> : null}{employee ? ` by ${employee}` : null} | Score: {score}</span>;
    } else {
        return null
    }
}

const SearchResult = props => (
    <div className="col card w-100 mb-2 border-light">
        <div className="card-body">
            <h5 className="card-title">
                <Link href={props.item.url}><a>{props.item.title}</a></Link>
            </h5>
            <h6 className="card-subtitle mb-1">
                <Link href={props.item.url}><a className="text-success">{props.item.url}</a></Link>
            </h6>
            <p className="card-text">
                {truncate(props.item.description, 250)}
                <br />
                <small className="text-muted" children={postedInfo(props.item.datePosted, props.item.hiredBy, props.score)}></small>
            </p>
        </div>
    </div>
)

export default SearchResult