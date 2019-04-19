import React, { Component } from 'react';


class App extends Component {
  state = {
    profile:[]
  };
  async componentDidMount() {
    try {
      const res = await fetch('http://127.0.0.1:8000/api/');
      const profile = await res.json();
      this.setState({
        profile
      });
    } catch (e) {
      console.log(e);
    }
  }
  render() {
    return (
      <div>
        {this.state.profile.map(item => (
          <div key={item.id}>
            <h1>{item.user}</h1>
            // fields = ('user', 'first_name', 'last_name ', 'licence_plate', 'email', 'phone', 'balance')
            <span>{item.first_name}</span>
          </div>
        ))}
      </div>
    );
  }
}

export default App;
