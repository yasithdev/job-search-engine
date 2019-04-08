import Header from './Header'
import Head from 'next/head';
import "../styles.scss"

const PageContainer = (props) => (
  <div className="container bg-light">
      <Head>
        <title>Job Search Engine</title>
        <meta name="viewport" content="initial-scale=1.0, width=device-width" />
        <link rel="stylesheet" href="https://use.fontawesome.com/releases/v5.8.1/css/all.css" integrity="sha384-50oBUHEmvpQ+1lW4y57PTFmhCaXp0ML5d60M1M7uH2+nqUivzIebhndOJK28anvf" crossorigin="anonymous"/>
    </Head>
    <Header />
    <div className="row">
      <div className="col">
        {props.children}
      </div>
    </div>
  </div>
)

export default PageContainer