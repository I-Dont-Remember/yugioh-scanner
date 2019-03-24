import React from "react"

import Layout from "../components/layout"
import SEO from "../components/seo"
import Deck from "../components/deck"
import { replace } from "gatsby";

const styles = {
    wrapper: {
        textAlign: "center"    
    }
}

function sumTds(tds) {
    let sum = 0;
    for (let i=0;i < tds.length; i++) {
        const text = tds[i].innerHTML;
        sum += (text === "None")? 0: parseFloat(text);
    }
    return sum;
}

const url = "https://cx05z8loqi.execute-api.us-east-1.amazonaws.com/dev/price"
class IndexPage extends React.Component {
    // cards is list of lists, each one has multiple subtypes: unlimited, 1st edition
    state = {
        cards: [],
        displayedSubTypes: {},
        totals: {
            market:0,
            low:0,
            mid:0,
            high:0
        }
    }

    // changeSelect = (event) => {

    // }

    // getTotals = () => {
    //     let totals =  {
    //         market:0,
    //         low:0,
    //         mid:0,
    //         high:0
    //     }
    //     const deck = document.getElementById("deck");
    //     if (deck) {
    //         const markets = document.getElementById("deck").getElementsByClassName("marketPrice");
    //         const lows = document.getElementById("deck").getElementsByClassName("lowPrice");
    //         const mids = document.getElementById("deck").getElementsByClassName("midPrice");
    //         const highs = document.getElementById("deck").getElementsByClassName("highPrice");
            
    //         totals.market = sumTds(markets);
    //         totals.low = sumTds(lows);
    //         totals.mid = sumTds(mids);
    //         totals.high = sumTds(highs);
    //     }
    //     console.log(totals)
    //     return totals
    // }

    handleChange = (event) => {
        this.setState({newCardNumber: event.target.value});
    }

    handleNewCardDown = (event) => {
        if (event.key !== 'Enter') {
            return;
        }

        event.preventDefault();
    
        const cards = this.state.cards;
        if (cards.length >= 50) {
            alert("No more than 60 cards for now");
            this.setState({newCardNumber: ""});
        } else {
            const number = this.state.newCardNumber.trim();
            
            if (number) {
                console.log("api call");
                const apiCall =  {
                    "cardNumber": "RDS-EN020",
                    "name": "Raging Flame Sprite",
                    "prices": [
                        {
                            "cardNumber": "RDS-EN020",
                            "highPrice": 1.0,
                            "lowPrice": 0.1,
                            "marketPrice": 0.5,
                            "midPrice": 0.2,
                            "name": "Raging Flame Sprite",
                            "productId": 23416,
                            "subTypeName": "Unlimited"
                        },
                        {
                            "cardNumber": "RDS-EN020",
                            "highPrice": 0.79,
                            "lowPrice": 0.11,
                            "marketPrice": 0.25,
                            "midPrice": 0.24,
                            "name": "Raging Flame Sprite",
                            "productId": 23416,
                            "subTypeName": "1st Edition"
                        }
                    ],
                    "productId": 23416,
                    "subTypes": [
                        "Unlimited",
                        "1st Edition"
                    ]
                }
                

                this.addCard(apiCall);
                // // fetch doesn't count 500 as an error, so check it
                // fetch(`${url}?number=${number}`)
                // .then(resp => {
                //     if (!resp.ok) {
                //         throw Error(resp.statusText);
                //     }
                //     console.log(resp);
                //     return resp.json();
                // })
                // .then((data) => {
                //     console.log(data);
                //     data.forEach(elem => {
                //         this.addCard(elem)
                //     })
                // })
                // .catch((error) => {
                //     if (error instanceof SyntaxError) {
                //         alert("Found nothing");
                //     } else {
                //         console.log(error);
                //         alert(error);
                //     }
                // })
            }
        }
    }

    addCard = (card) => {
        const cards = this.state.cards;
        card.id = `${Math.random()*500}-${Math.random()*500}-${Math.random()*500}`;
        cards.push(card);
        this.setState({newCardNumber: "", cards: cards});
    }

    removeCard = (id) => {
        this.setState({
            cards: this.state.cards.filter(c => { return c.id !== id})
        })
    }

    render() {
        const totals = this.state.totals;
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
            {/* <h3>Total</h3>
            <button onClick={this.updateTotals}>Refresh</button>
            <table>
                <thead>
                    <tr>
                        <th>Market</th>
                        <th>Low</th>
                        <th>Mid</th>
                        <th>high</th>
                    </tr>
                </thead>
                <tbody>
                    <tr>
                        <td>{totals.market}</td>
                        <td>{totals.low}</td>
                        <td>{totals.mid}</td>
                        <td>{totals.high}</td>
                    </tr>
                </tbody>
            </table> */}
        </div>
    </Layout>
    )}
}

export default IndexPage
