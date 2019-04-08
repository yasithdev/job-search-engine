import SearchResult from '../components/SearchResult';
import PageContainer from '../components/PageContainer';
import { withRouter } from 'next/router'
import Head from 'next/head'
import Link from 'next/link'
import SearchBar from '../components/SearchBar';
import QueryService from '../services/QueryService';

const pages = (from, size, total, window) => {
    if (from >= total) {
        return [];
    }
    const totalPages = Math.ceil(total / size);
    const activePage = Math.floor(from / size) + 1;
    const firstPageInWindow = Math.max(activePage - Math.floor(window / 2), 1);
    const lastPageInWindow = Math.min(firstPageInWindow + window, totalPages);
    const result = new Array(lastPageInWindow - firstPageInWindow + 1).fill().map((_, i) => i + firstPageInWindow);
    console.log(result);
    return result;
}


const Page = withRouter(props => (
    <PageContainer>
        <Head>
            <title>Job Search Engine - Search Results</title>
        </Head>
        <SearchBar text={props.router.query.query}></SearchBar>
        <small className="text-muted pt-0 px-1">{props.hits.total.toLocaleString()} results (in {props.took} ms)</small>
        <div className="pt-4">
            <nav aria-label="Page navigation example">
                <ul className="pagination justify-content-center">
                    <li className={`page-item ${props.pages.length == 0 || props.pages[1] == 1 ? 'disabled' : ''}`}>
                        <Link href={`/search?query=${props.router.query.query}&from=${props.size * (props.page - 2)}&size=${props.size}`}>
                            <a className="page-link" tabIndex="-1">&lt;</a>
                        </Link>
                    </li>
                    {props.pages.map(p => <li key={p} className={`page-item ${p == props.page ? 'active' : ''}`}>
                        <Link href={`/search?query=${props.router.query.query}&from=${props.size * (p - 1)}&size=${props.size}`}>
                            <a className="page-link">{p}</a>
                        </Link>
                    </li>)}
                    <li className={`page-item ${props.pages.length == 0 || props.pages[props.pages.length - 1] >= props.pages ? 'disabled' : ''}`}>
                        <Link href={`/search?query=${props.router.query.query}&from=${props.size * (props.page)}&size=${props.size}`}>
                            <a className="page-link" tabIndex="-1">&gt;</a>
                        </Link>
                    </li>
                </ul>
            </nav>
            {props.hits.hits.map(hit => <SearchResult key={hit._id} item={hit._source} score={hit._score} />)}
        </div>
    </PageContainer>
));

Page.getInitialProps = async function (props) {
    const query = props.query.query;
    const from = props.query.from || 0;
    const size = props.query.size || 10;
    const res = await new QueryService().query(query, from, size);
    const data = await res.json();
    data['pages'] = pages(from, size, data.hits.total, 5);
    data['from'] = from;
    data['page'] = Math.floor(from / size) + 1;
    data['size'] = size;
    return data;
}

export default Page