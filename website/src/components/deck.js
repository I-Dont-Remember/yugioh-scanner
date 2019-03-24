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

    getSelected = (id) => {
        const displayed = this.props.displayed;
        return displayed[id] || undefined;
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
                <Card key={c.id} card={c} remove={this.props.removeCard} onChange={this.props.selectOnChange} selected={this.getSelected(c.id)} />
                )
            )}
            </tbody>
        </table>
    )}
}

export default Deck