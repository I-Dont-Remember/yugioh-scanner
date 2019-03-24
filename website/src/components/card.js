import React from "react"

class Card extends React.Component {
    // state = {
    //     option: ""
    // }

    // selectOnChange = (event) => {
    //     const option = event.target.value;
    //     console.log("Change subtype: " + option);
    //     this.setState({option: option});
    //     // want to re-render parent when this updates
    //     // TODO: make this work this.props.updateTotals();
    // }

    // getCurrentFromOption = (option) => {
    //     const types = this.props.card.types;
    //     // find the correct subtype object from card
    //     for (let i in types) {
    //         if (types[i].subTypeName === option) {
    //             return types[i];
    //         }
    //     }
    //     return {};
    // }

    getPricesObject = (option) => {
        const prices = this.props.card.prices;
        if (!option) {
            return prices[0];
        }

        for (let i in prices) {
            if (prices[i].subTypeName === option) {
                return prices[i];
            }
        }

        console.log("failed to find matching subtype for " + JSON.stringify(option));
        return prices[0];
    }

    render() {
        // card is list of subtype objects
        const card = this.props.card;
        const selected = this.getPricesObject(this.props.selected);
        return (
        <tr>
            <td>{card.cardNumber}</td>
            <td>{card.name}</td>
            <td>
                <select
                    onChange={(event) => {this.props.onChange(event, card.id)}}
                    value={selected.subTypeName}
                >
                    {
                        card.subTypes.map(s=> (
                            <option key={Math.random()} value={s}>{s}</option>
                        ))
                    }
                </select>
            </td>
            <td className="marketPrice">{selected.marketPrice || "None"}</td>
            <td className="lowPrice">{selected.lowPrice || "None"}</td>
            <td className="midPrice">{selected.midPrice || "None"}</td>
            <td className="highPrice">{selected.highPrice || "None"}</td>
            <td><button  onClick={()=> {this.props.remove(card.id)}}>X</button></td>
        </tr>
    )}
}

export default Card