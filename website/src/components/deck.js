import React from 'react'
import Card from "../components/card"

const styles = {
    table: {
        width: "85%",
        marginLeft: "auto",
        marginRight: "auto"
    }
}

class Deck extends React.Component {

    removeCard = (card) => {
        this.props.removeCard(card);
    }

    render() {
        const cards = this.props.cards;
        return (
        <table id="deck" style={styles.table}>
            <thead>
                <tr>
                <th>Number</th>
                <th>Name</th>
                <th>SubType</th>
                <th>marketPrice</th>
                <th>lowPrice</th>
                <th>midPrice</th>
                <th>highPrice</th>
                <th></th>
                </tr>
            </thead>
            <tbody>
            {cards && cards.map(c => (
                <Card key={Math.random()} card={c} remove={this.removeCard} updateTotals={this.props.updateTotals}/>
                )
            )}
            </tbody>
        </table>
    )}
}

export default Deck