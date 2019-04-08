import Link from 'next/link'

const Header = (props) => (
  <nav className="navbar navbar-expand navbar-dark bg-dark mb-2">
    <a class="navbar-brand text-white">Job Search</a>
    <ul className="navbar-nav mr-auto">
      <li className="nav-item">
        <Link href="/"><a className="nav-link">Search</a></Link>
      </li>
      <li className="nav-item">
        <Link href="/about"><a className="nav-link">About</a></Link>
      </li>
    </ul>
  </nav>
)

export default Header