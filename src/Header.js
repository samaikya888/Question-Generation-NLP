import React, { Component }  from 'react';

const Header = (props) => { 
    return <header> 
    <h1>{props.title}</h1>
    <nav>
    <ul>
      <li><button onClick>Sign Up</button></li>
      <li><a href="#">Login</a></li>
    </ul>
  </nav> </header>;
}

export default Header;