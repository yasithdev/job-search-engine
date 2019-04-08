import Link from 'next/link'

const Header = (props) => (
  <nav className="navbar navbar-expand navbar-dark bg-dark mb-2">
    <Link href="/"><a className="navbar-brand">Job Search</a></Link>
    <ul className="navbar-nav mr-auto">
      <li className="nav-item">
        <Link href="/about"><a className="nav-link">About</a></Link>
      </li>
    </ul>
  </nav>
)

export default Header