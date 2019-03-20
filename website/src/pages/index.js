import React from "react"
import { Link } from "gatsby"

import Layout from "../components/layout"
import Image from "../components/image"
import SEO from "../components/seo"
import Deck from "../components/deck"

const styles = {
    wrapper: {
        textAlign: "center"    
    }
}
class IndexPage extends React.Component {
    state = {
        cards: [
            {number: "123-344"},
            {number: "345-dfdf"}
        ]
    }

    handleChange = (event) => {
        this.setState({newCardNumber: event.target.value});
    }

    handleNewCardDown = (event) => {
        if (event.key !== 'Enter') {
            return;
        }

        event.preventDefault();
    
        const number = this.state.newCardNumber.trim();

        if (number) {
            const cards = this.state.cards;
            if (cards.length >= 50) {
                alert("No more than 60 cards for now");
                return;
            }
            cards.push({number: number})

            this.setState({newCardNumber: "", cards: cards});
        }
    }

    removeCard = (card) => {
        this.setState({
            cards: this.state.cards.filter(c=> c.number !== card.number)
        })
    }

    render() {
        return (
    <Layout>
    <SEO title="Home" keywords={[`yugioh`, `deck prices`, `deck`]} />
        <div style={styles.wrapper}>
            <input
                placeholder="Add a card number.."
                value={this.state.newCardNumber}
                onKeyDown={this.handleNewCardDown}
                onChange={this.handleChange}
                autoFocus={true}
                />
            <Deck cards={this.state.cards} removeCard={this.removeCard} />
        </div>
    </Layout>
    )}
}

export default IndexPage
