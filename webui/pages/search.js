import SearchResult from '../components/SearchResult';
import PageContainer from '../components/PageContainer';
import { withRouter } from 'next/router'
import Head from 'next/head'
import fetch from 'isomorphic-unfetch'
import SearchBar from '../components/SearchBar';

const Page = withRouter(props => (
    <PageContainer>
        <Head>
            <title>Job Search Engine - Search Results</title>
        </Head>
        <SearchBar text={props.router.query.query}></SearchBar>
        <small className="text-muted pt-0 px-1">{props.hits.total.toLocaleString()} results (in {props.took} ms)</small>
        <div className="pt-4">
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