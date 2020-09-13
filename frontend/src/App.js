import React, { Component } from 'react'
import Instructions from './Instructions'
import Restaurant from './Restaurant'
import Counter from './Counter'

class App extends Component {
  constructor(props) {
    super(props)
    this.state = {
      restaurants: [
        {id: 1, name: "Golden Harbor", rating: 10},
        {id: 2, name: "Potbelly", rating: 6},
        {id: 3, name: "Noodles and Company", rating: 8},
      ],
	  newRestaurant: ""
    }
  }

  render() {
    return (
      <div className="App">
	  	<Counter count={0}/>
        <Instructions complete={true}/>
        {this.state.restaurants.map(x => (
          <Restaurant id={x.id} name={x.name} rating={x.rating} />
        ))}
		<input newRestaurant={this.state.newRestaurant} onChange={evt=>this.addRestaurant(evt)}/>
        <button type="button" onClick={this.handleSubmit}>Submit</button>
      </div>
    )
  }

  addRestaurant(evt) {
    this.setState({
      newRestaurant: evt.target.value
    });
  }

  handleSubmit = () => {
	this.setState((prevState) => ({restaurants: 
		[...prevState.restaurants, <Restaurant id={prevState.restaurants.length} 
		name={this.state.newRestaurant} rating={0} />]}));
  }

}

export default App
