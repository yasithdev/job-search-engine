import SearchResult from '../components/SearchResult';
import PageContainer from '../components/PageContainer';
import { withRouter } from 'next/router'
import fetch from 'isomorphic-unfetch'
import SearchBar from '../components/SearchBar';

const Page = withRouter(props => (
    <PageContainer>
        <SearchBar text={props.router.query.query}></SearchBar>
        <h2>{`Search Results for: ${props.router.query.query}`}</h2>
        {props.hits.map(hit => <SearchResult key={hit._id} item={hit._source} />)}
    </PageContainer>
));

Page.getInitialProps = async function (props) {
    const res = await fetch(`http://localhost:9200/postings/_search?q=${props.query.query}`)
    const data = await res.json()

    console.log(`Show data fetched. Count: ${data.hits.total}`)

    return {
        hits: data.hits.hits
    }
}

export default Page