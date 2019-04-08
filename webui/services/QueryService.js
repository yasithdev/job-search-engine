import fetch from 'isomorphic-unfetch'

class QueryService {
    async query(text, from, size) {
        return await fetch(`http://localhost:9200/postings/_search?q=${text}&from=${from}&size=${size}`);
    }
}

export default QueryService