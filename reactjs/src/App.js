import logo from './logo.svg';
import './App.css';
import "bootstrap/dist/css/bootstrap.min.css";
import { Routes, Route, Link } from 'react-router-dom';
import Home from './components/home';
import Login from './components/login';
import Dashboard from './components/dashboard';




function App() {
  return (
    <div>
      <nav className="navbar navbar-expand-sm navbar-dark bg-dark">
        <ul className="navbar-nav">
          <li className="nav-item">
            <Link className="nav-link" to="/">HOME</Link>
          </li>
          <li className="nav-item">
            <Link className="nav-link" to="/login">LOGIN</Link>
          </li>
          <li className="nav-item">
            <Link className="nav-link" to="/dashboard">DASHBOARD</Link>
          </li>
        </ul>

      </nav>
      <div className='container'>
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/login" element={<Login />} />
          <Route path="/dashboard" element={<Dashboard />} />
        </Routes>
      </div>
    </div>
  );
}

export default App;
