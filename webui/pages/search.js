import SearchResult from '../components/SearchResult';
import PageContainer from '../components/PageContainer';
import { withRouter } from 'next/router'
import fetch from 'isomorphic-unfetch'
import SearchBar from '../components/SearchBar';

const Page = withRouter(props => (
    <PageContainer>
        <SearchBar text={props.router.query.query}></SearchBar>
        <small className="text-muted pt-2 pb-4">{props.hits.total} results (in {props.took} ms)</small>
        <div>
            {props.hits.hits.map(hit => <SearchResult key={hit._id} item={hit._source} score={hit._score} />)}
        </div>
    </PageContainer>
));

Page.getInitialProps = async function (props) {
    const res = await fetch(`http://localhost:9200/postings/_search?q=${props.query.query}`)
    const data = await res.json()
    return data
}

export default Page