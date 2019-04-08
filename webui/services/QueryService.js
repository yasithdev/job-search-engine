import fetch from 'isomorphic-unfetch'

class QueryService {
    async query(text) {
        return await fetch(`http://localhost:9200/postings/_search?q=${text}`);
    }
}

export default QueryService