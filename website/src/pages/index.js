import React from "react"

import Layout from "../components/layout"
import SEO from "../components/seo"
import Deck from "../components/deck"
import { replace } from "gatsby";
import CircularProgress from '@material-ui/core/CircularProgress'
import Table from '@material-ui/core/Table';
import TableBody from '@material-ui/core/TableBody';
import TableCell from '@material-ui/core/TableCell';
import TableHead from '@material-ui/core/TableHead';
import TableRow from '@material-ui/core/TableRow';

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

function getId() {
    return Math.floor(Math.random()*500);
}

function calculateTotals(cards, displayed) {
    let totals =  {
        market:0,
        low:0,
        mid:0,
        high:0
    }

    for (let i in cards) {
        const selected = displayed[cards[i].id];
        // find the selected price in list
        for (let j in cards[i].prices) {
            const data = cards[i].prices[j];
            if (data.subTypeName === selected) {
                totals.market += data.marketPrice;
                totals.low += data.lowPrice;
                totals.mid += data.midPrice;
                totals.high += data.highPrice;
            }
        }
    }
    return totals;
}

class IndexPage extends React.Component {
    // cards is list of lists, each one has multiple subtypes: unlimited, 1st edition
    state = {
        isLoading: false,
        cards: [],
        displayedSubTypes: {},
        totals: {
            market:0,
            low:0,
            mid:0,
            high:0
        }
    }

    selectOnChange = (event, id) => {
        // safely update the displayed map
        const option = event.target.value;
        this.setState(prevState => {
            const updateDisplayed = {
                ...prevState.displayedSubTypes,
                [id]: option
            };
    
            return {
            displayedSubTypes: updateDisplayed,
            totals: calculateTotals(this.state.cards, updateDisplayed)
            }
        })
    }

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
                // const apiCall =  {
                //     "cardNumber": "RDS-EN020",
                //     "name": "Raging Flame Sprite",
                //     "prices": [
                //         {
                //             "cardNumber": "RDS-EN020",
                //             "highPrice": 1.0,
                //             "lowPrice": 0.1,
                //             "marketPrice": 0.5,
                //             "midPrice": 0.2,
                //             "name": "Raging Flame Sprite",
                //             "productId": 23416,
                //             "subTypeName": "Unlimited"
                //         },
                //         {
                //             "cardNumber": "RDS-EN020",
                //             "highPrice": 0.79,
                //             "lowPrice": 0.11,
                //             "marketPrice": 0.25,
                //             "midPrice": 0.24,
                //             "name": "Raging Flame Sprite",
                //             "productId": 23416,
                //             "subTypeName": "1st Edition"
                //         }
                //     ],
                //     "productId": 23416,
                //     "subTypes": [
                //         "Unlimited",
                //         "1st Edition"
                //     ]
                // }
                
                // this.addCard(apiCall);
                // fetch doesn't count 500 as an error, so check it
                this.setState({isLoading: true});
                fetch(`${url}?number=${number}`)
                .then(resp => {
                    if (!resp.ok) {
                        throw Error(resp.statusText);
                    }
                    console.log(resp);
                    return resp.json();
                })
                .then((data) => {
                    console.log(data);
                    this.addCard(data);
                })
                .catch((error) => {
                    if (error instanceof SyntaxError) {
                        alert("Found nothing");
                    } else {
                        console.log(error);
                        alert(error);
                    }
                })
                .then(()=> {
                    console.log("finally setting loading to false")
                    this.setState({isLoading: false})
                })
            }
        }
    }

    addCard = (card) => {
        // safely add to cards list and displayed map
        let cards = this.state.cards.slice();
        card.id = `${getId()}-${getId()}-${getId()}`;
        cards.push(card);
        this.setState(prevState => {
            const updateDisplayed = {
                ...prevState.displayedSubTypes,
                [card.id]: card.prices[0].subTypeName
            };
            return {
                newCardNumber: "", 
                cards: cards,
                displayedSubTypes: updateDisplayed,
                totals: calculateTotals(cards, updateDisplayed)
            }
        });
    }

    removeCard = (id) => {
        // safely remove item from both cards list and displayed map
        let cards = this.state.cards.filter((item) => {
            return item.id !== id
        })
        let updateDisplayed = Object.assign({}, this.state.displayedSubTypes);
        delete updateDisplayed[id];
        this.setState({
            cards: this.state.cards.filter(c => { return c.id !== id}),
            displayedSubTypes: updateDisplayed,
            totals: calculateTotals(cards, updateDisplayed)
        })
    }

    render() {
        console.log(this.state);
        const totals = this.state.totals;
        return (
    <Layout>
    <SEO title="Home" keywords={[`yugioh`, `deck prices`, `deck`]} />
        <div style={styles.wrapper}>
            {this.state.isLoading? 
                <CircularProgress />
                : <input
                placeholder="Add a card number.."
                value={this.state.newCardNumber}
                onKeyDown={this.handleNewCardDown}
                onChange={this.handleChange}
                autoFocus={true}
                />}
            <br />
            <br />
            <Deck cards={this.state.cards} removeCard={this.removeCard} selectOnChange={this.selectOnChange} displayed={this.state.displayedSubTypes} />
            <br />
            <h3>Totals</h3>
            <Table>
                <TableHead>
                    <TableRow>
                        <TableCell>Market</TableCell>
                        <TableCell>Low</TableCell>
                        <TableCell>Mid</TableCell>
                        <TableCell>High</TableCell>
                    </TableRow>
                </TableHead>
                <TableBody>
                    <TableRow>
                        <TableCell>$ {totals.market}</TableCell>
                        <TableCell>$ {totals.low}</TableCell>
                        <TableCell>$ {totals.mid}</TableCell>
                        <TableCell>$ {totals.high}</TableCell>
                    </TableRow>
                </TableBody>
            </Table>
                {/* <thead>
                    <tr>
                        <th>Market</th>
                        <th>Low</th>
                        <th>Mid</th>
                        <th>High</th>
                    </tr>
                </thead>
                <tbody>
                    <tr>
                        <td>${totals.market}</td>
                        <td>${totals.low}</td>
                        <td>${totals.mid}</td>
                        <td>${totals.high}</td>
                    </tr>
                </tbody>
                </table> */}
        </div>
    </Layout>
    )}
}

export default IndexPage
