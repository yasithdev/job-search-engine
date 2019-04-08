import SearchResult from '../components/SearchResult';
import PageContainer from '../components/PageContainer';
import { withRouter } from 'next/router'
import Head from 'next/head'
import SearchBar from '../components/SearchBar';
import QueryService from '../services/QueryService';

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

Page.defaultProps = {
    queryService: new QueryService()
}

Page.getInitialProps = async function (props) {
    const res = await new QueryService().query(props.query.query)
    const data = await res.json()
    return data
}

export default Page